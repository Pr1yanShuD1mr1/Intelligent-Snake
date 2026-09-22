from ae import Game
from ar import Agent

if __name__ == "__main__":

    agent = Agent()
    game = Game(agent=agent)
    n_games = 10

    try:
        for i in range(n_games):
            agent.set_elipson(0.01)
            game.Run(debugOutput=True)
            agent.learn()
            agent.model.save()
    finally:
        agent.model.save()




