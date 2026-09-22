from ae import Game
from ar import Agent
from gr import plot


if __name__ == "__main__":

    agent = Agent()
    game = Game(agent=agent)

    n_games = 0     # no of games
    t_games = 100   # training period of game 
    
    highest_score       = 0
    cummilative_score   = 0
    record_score        = [0]
    record_mean_score   = [0]

    try:
        while n_games < t_games:

            plot(record_score, record_mean_score)

            agent.set_elipson(max(0, t_games-n_games))
            game.Run()
            agent.learn()

            n_games += 1
            highest_score = max(highest_score, game.score)

            cummilative_score += game.score
            mean_score = cummilative_score / n_games
            record_score.append(game.score)
            record_mean_score.append(mean_score)
            agent.model.save()

    finally:
        agent.model.save()




