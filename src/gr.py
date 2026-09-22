import matplotlib.pyplot as plt
from IPython import display

plt.ion()
fig, ax = plt.subplots(figsize=(8, 5))

def plot(scores, mean_scores):
    ax.clear()
    
    ax.set_title('Training Progress', fontsize=14)
    ax.set_xlabel('Number of Games')
    ax.set_ylabel('Score')
    
    ax.plot(scores, label='Score', color='dodgerblue', alpha=0.6)
    ax.plot(mean_scores, label='Mean Score', color='darkorange', linewidth=2)
    ax.legend(loc='upper left')
    
    ax.set_ylim(ymin=0)
    
    if len(scores) > 0 and len(mean_scores) > 0:
        ax.text(len(scores)-1, scores[-1], f"{scores[-1]:.1f}", color='blue')
        ax.text(len(mean_scores)-1, mean_scores[-1], f"{mean_scores[-1]:.1f}", color='red')
    
    display.clear_output(wait=True)
    display.display(fig)
    
    plt.pause(0.01)