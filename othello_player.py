import requests
import sys
import time

from src.game_engine.board import print_board
from othello_ai import ai_move  # Asegúrate de tener esta función implementada

# URL del servidor backend
BASE_URL = "https://7b679617-8c6b-4d0f-bb51-0505412c6c17.us-east-1.cloud.genez.io"

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Uso: python othello_player.py <NombreTorneo> <NombreUsuario>")
        sys.exit(1)

    tournament_name = sys.argv[1]
    username = sys.argv[2]

    print("Solicitando unirse al torneo...")
    req = requests.post(f"{BASE_URL}/tournament/join", json={
        'username': username,
        'tournament_name': tournament_name
    })

    if req.status_code == 409:
        print(f"⚠️ {req.json().get('detail', 'Error al unirse al torneo')}")
        sys.exit(1)

    if req.status_code == 200:
        print(f"✅ Bienvenido al torneo {tournament_name}, {username}. Esperando a que comience la partida...")

        while True:
            active = requests.post(f"{BASE_URL}/match/active", json={
                'username': username,
                'tournament_name': tournament_name
            })

            if active.json().get('is_in_active_match'):
                while True:
                    status = requests.post(f"{BASE_URL}/match/status", json={
                        'username': username,
                        'tournament_name': tournament_name
                    })

                    if status.status_code == 404:
                        break  # La partida terminó
                    elif status.status_code == 409:
                        time.sleep(2)  # No es tu turno
                    elif status.status_code == 200:
                        response = status.json()

                        if response['msg'] == 'Match ended':
                            print(f"🏁 La partida ha terminado. Ganador: {response['winner']}")
                            break
                        else:
                            board = response['board']
                            player = response['player_color']
                            print("\n====================================")
                            print(f"Turno de {'Negro ○' if player == -1 else 'Blanco ●'}")
                            print("Tablero actual:")
                            print_board(board)

                            start = time.perf_counter()
                            move = ai_move(board, player)
                            elapsed = time.perf_counter() - start
                            print(f"Movimiento elegido: {move} (en {elapsed:.2f} segundos)")
                            print("====================================")

                            if move is None:
                                print("No hay movimientos posibles. Turno pasado.")
                                break
                            else:
                                res = requests.post(f"{BASE_URL}/match/move", json={
                                    "username": username,
                                    "tournament_name": tournament_name,
                                    "x": move[0],
                                    "y": move[1]
                                })

                                if res.status_code == 409:
                                    print("⚠️ ¡Movimiento inválido!")
                                else:
                                    print("✅ Movimiento realizado.")
                                    break  

            else:
                print("Esperando tu siguiente partida...")
                time.sleep(10)
