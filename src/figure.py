import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

def draw_lineplot(agent1_ratings, agent2_ratings, key, result_dir):
    agent1_ratings = np.array(agent1_ratings)
    agent2_ratings = np.array(agent2_ratings)

    # Compute mean and standard error (SE)
    agent1_mean = np.mean(agent1_ratings, axis=0)
    agent1_se = np.std(agent1_ratings, axis=0) / np.sqrt(agent1_ratings.shape[0])

    agent2_mean = np.mean(agent2_ratings, axis=0)
    agent2_se = np.std(agent2_ratings, axis=0) / np.sqrt(agent2_ratings.shape[0])

    rounds = np.arange(1, len(agent1_mean) + 1)

    # Flatten data for regression
    agent1_x = np.array(list(rounds)*agent1_ratings.shape[0])
    agent1_y = agent1_ratings.flatten()

    agent2_x = np.array(list(rounds)*agent2_ratings.shape[0])
    agent2_y = agent2_ratings.flatten()

    # Perform linear regression
    agent1_slope, agent1_intercept, agent1_r, agent1_p, _ = stats.linregress(agent1_x, agent1_y)
    agent2_slope, agent2_intercept, agent2_r, agent2_p, _ = stats.linregress(agent2_x, agent2_y)

    # Create regression lines
    agent1_fit = agent1_slope * rounds + agent1_intercept
    agent2_fit = agent2_slope * rounds + agent2_intercept

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(rounds, agent1_mean, label="Agent 1", color='blue')
    plt.fill_between(rounds, agent1_mean - agent1_se, agent1_mean + agent1_se, color='blue', alpha=0.2)

    plt.plot(rounds, agent2_mean, label="Agent 2", color='red')
    plt.fill_between(rounds, agent2_mean - agent2_se, agent2_mean + agent2_se, color='red', alpha=0.2)

    # Plot regression lines
    plt.plot(rounds, agent1_fit, '--', color='blue', label=f"Agent 1 Fit: y={agent1_slope:.2f}x+{agent1_intercept:.2f}, p={agent1_p:.2f}")
    plt.plot(rounds, agent2_fit, '--', color='red', label=f"Agent 2 Fit: y={agent2_slope:.2f}x+{agent2_intercept:.2f}, p={agent2_p:.2f}")

    plt.xlabel("Round")
    plt.ylabel(f"Average {key[0].upper()+key[1:]} Level")
    plt.title(f"Comparison of {key[0].upper()+key[1:]} Level Between Agent 1 and Agent 2 (with Standard Error)")
    plt.legend()
    plt.grid(True)

    # Show plot
    plt.show()

    # save the figure
    plt.savefig(f"{result_dir}{key}.png")