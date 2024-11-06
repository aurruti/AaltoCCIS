from PIL import Image, ImageDraw
import numpy as np
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

def create_button_color(width, height, colour):
    """
    Generate a button with the specified color.
    
    :param width: Width of the button.
    :param height: Height of the button.
    :param colour: RGB tuple representing the button color.
    :return: An Image object containing the button.
    """
    button = Image.new("RGB", (int(width), int(height)))
    draw = ImageDraw.Draw(button)


    colour = tuple(map(int, np.clip(colour, 0, 255).flatten().tolist()))

    draw.rectangle([0, 0, width, height], fill=colour)
    
    return button

def overlay_color_picker_plus_button(image_path, rgb_distribution, button_colour, bar_height=35, position=(75, 385), width=230, button_width=58, button_height=42, button_position=(235, 269)):
    """
    Overlay the color picker bar and the button overlay onto an image.
    
    :param image_path: Path to the image file.
    :param rgb_distribution: A list of RGB tuples to represent colors across the bar.
    :param button_colour: RGB tuple representing the button color.
    :param bar_height: Height of the color picker bar.
    :param position: (x, y) position to place the color picker bar on the image.
    :param width: Width of the color picker bar.
    :param button_width: Width of the button.
    :param button_height: Height of the button.
    :param button_position: (x, y) position to place the button on the image.
    :return: An Image object with the color picker bar overlay.
    """
    base_image = Image.open(image_path)
    color_picker_bar = create_color_picker_bar(width, bar_height, rgb_distribution)
    button = create_button_color(button_width, button_height, button_colour)
    base_image.paste(color_picker_bar, position)
    base_image.paste(button, button_position)
    
    return base_image

def display_image(rgb_distribution, button_color, image_path="base_screen.png"):
    image = overlay_color_picker_plus_button(image_path, rgb_distribution, button_color)
    plt.imshow(image)
    plt.axis('off')
    plt.show()

def get_designer_rating_bar():
    try:
        rating = float(input("Rate this color bar from 0 to 5: "))
        if 0 <= rating <= 5:
            return rating
        else:
            print("Invalid rating. Please enter a number between 0 and 5.")
            return get_designer_rating_bar()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return get_designer_rating_bar()

def get_designer_rating_button():
    try:
        rating = float(input("Rate this color button from 0 to 5: "))
        if 0 <= rating <= 5:
            return rating
        else:
            print("Invalid rating. Please enter a number between 0 and 5.")
            return get_designer_rating_button()
    except ValueError:
        print("Invalid input. Please enter a number.")
        return get_designer_rating_button()

if __name__ == "__main__":
    bounds_rgb = torch.tensor([[0.0, 0.0, 0.0], [255.0, 255.0, 255.0]])  # RGB bounds
    bounds_button = torch.tensor([[0.0, 0.0, 0.0], [255.0, 255.0, 255.0]])  # Button color bounds
    bounds = torch.cat([bounds_rgb, bounds_button], dim=0)

    num_colors = 7  # Number of colors in the RGB picker bar
    initial_samples = 5
    iterations = 10

    train_X_bar = []
    train_Y_bar = []
    train_X_button = []
    train_Y_button = []

    ## Display a random sample image
    #rgb_distribution = torch.rand(num_colors, 3) * 255
    #button_color = torch.rand(3) * 255
    #display_image(rgb_distribution, button_color)

    # Double optimization and pareto front
    for i in range(initial_samples):
        color_distribution = torch.randint(0, 256, (num_colors, 3)).float()  # Random initial RGB distribution
        button_colour = torch.randint(0, 256, (3,)).float()  # Random initial button color
        color_distribution_tuple = tuple(map(tuple, color_distribution.numpy())) 
        display_image(color_distribution_tuple, button_colour)
        rating_bar = get_designer_rating_bar()
        rating_button = get_designer_rating_button()
        train_X_bar.append(color_distribution.flatten())
        train_Y_bar.append(rating_bar)
        train_X_button.append(button_colour)
        train_Y_button.append(rating_button)

    train_X_bar = torch.stack(train_X_bar)
    train_Y_bar = torch.tensor(train_Y_bar).unsqueeze(-1)
    train_X_button = torch.stack(train_X_button)
    train_Y_button = torch.tensor(train_Y_button).unsqueeze(-1)

    # Bayesian Optimization Loop
    for i in range(iterations):
        gp1 = SingleTaskGP(train_X_bar, train_Y_bar)
        mll1 = ExactMarginalLogLikelihood(gp1.likelihood, gp1)
        gp1.train()
        mll1.train()
        optimizer1 = torch.optim.Adam(gp1.parameters(), lr=0.1)
        optimizer1.zero_grad()
        output1 = gp1(train_X_bar)
        loss1 = -mll1(output1, train_Y_bar).sum()  # Ensure loss is a scalar
        loss1.backward()
    
        gp2 = SingleTaskGP(train_X_button, train_Y_button)
        mll2 = ExactMarginalLogLikelihood(gp2.likelihood, gp2)
        gp2.train()
        mll2.train()
        optimizer2 = torch.optim.Adam(gp2.parameters(), lr=0.1)
        optimizer2.zero_grad()
        output2 = gp2(train_X_button)
        loss2 = -mll2(output2, train_Y_button).sum()  # Ensure loss is a scalar
        loss2.backward()

        with torch.no_grad():
            optimizer1.step()
            optimizer2.step()
        
        # Acquisition function with higher exploitation
        EI1 = LogExpectedImprovement(gp1, best_f=train_Y_bar.max()) 
        EI2 = LogExpectedImprovement(gp2, best_f=train_Y_button.max())
        
        # Next candidate
        candidate1, _ = optimize_acqf(
            EI1,
            bounds=torch.tensor([[0.0] * (num_colors * 3), [255.0] * (num_colors * 3)]),  
            q=1,
            num_restarts=10,  
            raw_samples=50,   
        )
        candidate2, _ = optimize_acqf(
            EI2,
            bounds=bounds_button,
            q=1,
            num_restarts=10,
            raw_samples=50,
        )

        # Display candidate to the designer
        rgb_distribution = candidate1.detach().reshape(num_colors, 3).numpy()
        rgb_distribution_tuple = tuple(map(tuple, rgb_distribution)) 
        button_colour = candidate2.numpy()
        display_image(rgb_distribution, button_colour)
        
        # Get Rating
        rating1 = get_designer_rating_bar()
        rating2 = get_designer_rating_button()
        
        # New training data
        train_X_bar = torch.cat([train_X_bar, candidate1])
        train_Y_bar = torch.cat([train_Y_bar, torch.tensor([[rating1]])])
        train_X_button = torch.cat([train_X_button, candidate2])
        train_Y_button = torch.cat([train_Y_button, torch.tensor([[rating2]])])


    # Plot Pareto Front
    best_indices = torch.topk(train_Y_bar.squeeze() + train_Y_button.squeeze(), 3).indices
    best_points = torch.stack([train_Y_bar[best_indices], train_Y_button[best_indices]]).numpy()

    plt.scatter(train_Y_bar.numpy(), train_Y_button.numpy())
    plt.xlabel('Bar Rating')
    plt.ylabel('Button Rating')
    plt.title('Pareto Front')
    plt.show()

    # Show sample 3 best solutions
    best_indices = torch.topk(train_Y_bar.squeeze() + train_Y_button.squeeze(), 3).indices
    for idx in best_indices:
        best_color_distribution = train_X_bar[idx].view(num_colors, 3)
        best_button_color = train_X_button[idx]
        display_image(best_color_distribution.numpy(), best_button_color.numpy())

            
               
