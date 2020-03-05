from starlette.responses import UJSONResponse
from starlette.routing import Route
from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response

from boggle.defaults import DEFAULT_BOARD, DICTIONARY
from boggle.exceptions import InvalidUsage, NotFound, Forbidden
from boggle.models import Board, unix_time
from boggle.utils.authentication import authenticate
from boggle.utils.serialization import serialize_response
from boggle.utils.views.game import exist, parse_matrix, calculate_word_points
from boggle.utils.validation import validate_request


class Gameplay(HTTPEndpoint):
    @serialize_response(model="Board")
    @validate_request(model="Board", method="Read")
    async def get(self, *args, path_params=None, **kwargs):
        """
        summary: Return the board with the given ID.
        parameters:
          - name: id
            in: path
            description: The ID of the board.
            schema:
              type : integer
              format: int64
              minimum: 1

        responses:
          200:
            description: The requested Board.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    id:
                      type: integer
                      description: The Board ID.
                    token:
                      type: string
                      description: The token used for authentication on playing the board.
                    board:
                      type: string
                      description: A string representing the board of the game.
                    duration:
                      type: integer
                      description: The time (in seconds) that specifies the duration of the game.
                    time_left:
                      type: integer
                      description: The time until you could not play the board anymore.
                    points:
                      type: integer
                      description: The total points of the board.
                  example:
                    id: 1
                    token: 9dda26ec7e476fb337cb158e7d31ac6c
                    duration: 12345
                    board: A, C, E, D, L, U, G, *, E, *, H, T, G, A, F, K
                    time_left: 10000
                    points: 10
        """

        board_id = path_params["id"]
        board = await Board.get(id=board_id)

        # Object validation
        if not board:
            raise NotFound("There is no game with current ID")

        current_duration = unix_time() - board["created_at"]
        time_left = board["duration"] - current_duration

        return {
            **board,
            "time_left": time_left if time_left else 0,
        }

    @serialize_response(model="Board")
    @validate_request(model="Board", method="Read")
    @authenticate
    async def put(self, *args, path_params, body, **kwargs):
        """
        summary: Play the board with the given ID.
        requestBody:
          content:
            application/json:
              schema:
                type: object
                properties:
                    token:
                        type: string
                        description: The token used for authentication on playing the board.
                    word:
                        type: string
                        description: The word used to play.

        responses:
          200:
            description:
                The Board with updated points.
                The points will not change if the word is not valid.
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    id:
                      type: integer
                      description: The Board ID.
                    token:
                      type: string
                      description: The token used for authentication on playing the board.
                    board:
                      type: string
                      description: A string representing the board of the game.
                    duration:
                      type: integer
                      description: The time (in seconds) that specifies the duration of the game
                    time_left:
                      type: integer
                      description: The time until you could not play the board anymore.
                    points:
                      type: integer
                      description: The total points of the board.
                  example:
                    id: 1
                    token: 9dda26ec7e476fb337cb158e7d31ac6c
                    duration: 12345
                    board: A, C, E, D, L, U, G, *, E, *, H, T, G, A, F, K
                    time_left: 10000
                    points: 10
        """
        if "id" not in path_params:
            raise InvalidUsage("Missing ID in path params")

        if "word" not in body:
            raise InvalidUsage("Missing required parameters")

        if not isinstance(body["word"], str):
            raise InvalidUsage("Parameter 'word' must be a string.")

        search_word = body["word"]
        if search_word not in DICTIONARY:
            raise InvalidUsage(
                f"The word '{search_word}' is not found in the dictionary"
            )

        board_id = path_params["id"]
        board_data = await Board.get(id=board_id)

        current_duration = unix_time() - board_data["created_at"]
        time_left = board_data["duration"] - current_duration
        if time_left <= 0:
            raise Forbidden("The duration for playing this board has ended.")

        # Object validation
        if not board_data:
            raise NotFound("There is no game with current ID")

        # Board parsing:
        new_board = parse_matrix(board_data["board"])

        if exist(new_board, search_word):
            new_point = board_data["points"] + calculate_word_points(search_word)
            board_data = await Board.modify({"id": board_id}, {"points": new_point})

        return {
            **board_data,
            "time_left": time_left,
        }


@serialize_response(model="Board", status_code=201)
@validate_request(model="Board", method="Write")
async def create_game(*args, body, **kwargs):
    """
    summary: Play the board with the given ID.
    requestBody:
        content:
            application/json:
                schema:
                  type: object
                  properties:
                    duration:
                        type: integer
                        description:
                            The time (in seconds) that specifies the duration of the game
                    random:
                        type: boolean
                        description:
                            If true, then the game will be generated with random board.
                            Otherwise, it will be generated based on input.
                    board:
                        type: string
                        description:
                            If random is not true, this will be used as the board for new game.
                            If this is not present, new game will get the default board.
    responses:
      201:
        description: The created Board.
        content:
          application/json:
            schema:
              type: object
              properties:
                id:
                  type: integer
                  description: The Board ID.
                token:
                  type: string
                  description: The token used for authentication on playing the board.
                board:
                  type: string
                  description: A string representing the board of the game.
                duration:
                  type: integer
                  description: The time (in seconds) that specifies the duration of the game.
                time_left:
                  type: integer
                  description: The time until you could not play the board anymore.
                points:
                  type: integer
                  description: The total points of the board.
              example:
                id: 1
                token: 9dda26ec7e476fb337cb158e7d31ac6c
                duration: 12345
                board: A, C, E, D, L, U, G, *, E, *, H, T, G, A, F, K
                time_left: 10000
                points: 10
    """

    if "duration" not in body and "random" not in body:
        raise InvalidUsage("Missing required parameters")

    duration = body["duration"]
    random = body["random"]

    if "board" in body and not random:
        input_board = body["board"]
        return await Board.add(duration=duration, board=input_board)

    return await Board.add(duration=duration, board=DEFAULT_BOARD)


routes = [
    Route("/games", endpoint=create_game, methods=["POST"]),
    Route("/games/{id}", endpoint=Gameplay, methods=["GET", "PUT"]),
]
