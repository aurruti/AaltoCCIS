from PIL import Image, ImageDraw
import torch
from botorch.models import SingleTaskGP
from botorch.acquisition import LogExpectedImprovement
from botorch.optim import optimize_acqf
from gpytorch.mlls import ExactMarginalLogLikelihood
import matplotlib.pyplot as plt


def create_color_picker_bar(width, height, rgb_distribution):
    """
    Generate an RGB color picker bar based on the input color distribution.
    
    :param width: Width of the bar.
    :param height: Height of the bar.
    :param rgb_distribution: A list of RGB tuples to represent colors across the bar.
    :return: An Image object containing the RGB color picker bar.
    """
    color_picker_bar = Image.new("RGB", (int(width), int(height)))
    draw = ImageDraw.Draw(color_picker_bar)
    segment_width = width // len(rgb_distribution)
    
    # Draw each color segment onto the bar
    for i, color in enumerate(rgb_distribution):
        start_x = int(i * segment_width)
        end_x = int(start_x + segment_width)
        draw.rectangle([start_x, 0, end_x, height], fill=tuple(map(int, color)))
    
    return color_picker_bar

def overlay_color_picker(image_path, rgb_distribution, bar_height=50, position=(0, 0), width=230):
    """
    Overlay the color picker bar onto an image.
    
    :param image_path: Path to the image file.
    :param rgb_distribution: A list of RGB tuples to represent colors across the bar.
    :param bar_height: Height of the color picker bar.
    :param position: (x, y) position to place the color picker bar on the image.
    :param width: Width of the color picker bar.
    :return: An Image object with the color picker bar overlay.
    """
    base_image = Image.open(image_path)
    color_picker_bar = create_color_picker_bar(width, bar_height, rgb_distribution)
    base_image.paste(color_picker_bar, position)
    
    return base_image

def display_image_with_color_picker(rgb_distribution, image_path="base_screen.png"):
    image_with_color_picker = overlay_color_picker(image_path, rgb_distribution, bar_height=35, position=(75, 385))
    plt.imshow(image_with_color_picker)
    plt.axis('off')
    plt.show()

def get_designer_rating():
    try:
        rating = float(input("Rate this color scheme from 0 to 5: "))
        if 0 <= rating <= 5:
            return rating
        else:
            print("Invalid rating. Please enter a number between 0 and 5.")
            return get_designer_rating()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return get_designer_rating()

if __name__ == "__main__":
    bounds = torch.tensor([[0.0, 0.0, 0.0], [255.0, 255.0, 255.0]])  # RGB range per color component
    num_colors = 7  # Number of colors in the RGB picker bar
    initial_samples = 5  # Initial random samples to kickstart BO
    iterations = 10  # Number of BO iterations

    # Collect initial data
    train_X = []
    train_Y = []
    for _ in range(initial_samples):
        color_distribution = torch.randint(0, 256, (num_colors, 3)).float()  # Random initial RGB distribution
        color_distribution_tuple = tuple(map(tuple, color_distribution.numpy())) 
        display_image_with_color_picker(color_distribution_tuple)
        rating = get_designer_rating()
        train_X.append(color_distribution.flatten())
        train_Y.append(rating)

    train_X = torch.stack(train_X)
    train_Y = torch.tensor(train_Y).unsqueeze(-1)

    # Bayesian Optimization Loop
    for i in range(iterations):
        gp = SingleTaskGP(train_X, train_Y)
        mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
        gp.train()
        mll.train()
        optimizer = torch.optim.Adam(gp.parameters(), lr=0.1)
        optimizer.zero_grad()
        output = gp(train_X)
        loss = -mll(output, train_Y).sum()  # Ensure loss is a scalar
        loss.backward()
        with torch.no_grad():
            optimizer.step()
        
        # Acquisition function with higher exploitation
        EI = LogExpectedImprovement(gp, best_f=train_Y.max()) 
        
        # Next candidate
        candidate, _ = optimize_acqf(
            EI,
            bounds=torch.cat([bounds] * num_colors, dim=1),  
            q=1,
            num_restarts=10,  
            raw_samples=50,   
        )
        
        # Display candidate to the designer
        rgb_distribution = candidate.detach().reshape(num_colors, 3).numpy()
        rgb_distribution_tuple = tuple(map(tuple, rgb_distribution)) 
        display_image_with_color_picker(rgb_distribution_tuple)
        
        # Get Rating
        rating = get_designer_rating()
        
        # New training data
        train_X = torch.cat([train_X, candidate])
        train_Y = torch.cat([train_Y, torch.tensor([[rating]])])

    print("Optimization complete.")
    # Show best color scheme
    best_idx = train_Y.argmax()
    best_color_scheme = train_X[best_idx].reshape(num_colors, 3).numpy()
    display_image_with_color_picker(tuple(map(tuple, best_color_scheme)))