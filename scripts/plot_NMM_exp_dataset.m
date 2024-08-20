
load('NMM_exp_dataset.mat')
surf(t, q, iso)

%title('Sample Plot', 'FontSize', 16); % Increase font size for title

fsize = 16;
xlabel('t (ps)', 'FontSize', fsize)
ylabel('q (Å^{-1})', 'FontSize', fsize)
zlabel('%ΔI(q,t)', 'FontSize', fsize)

% Customize the axes ticks
set(gca, 'FontSize', 14); % Increase font size for tick labels

% Set the maximum height of the plot
maxHeight = 1.1; % Define the maximum height
zlim([min(iso(:)) maxHeight]); % Set the z-axis limits

% Rotate the view
view(-45, 70); % Set the view angle: 45 degrees azimuth, 30 degrees elevation

% Save the plot as a high-resolution PNG
print('high_resolution_plot_70', '-dpng', '-r300'); % '-r300' sets the resolution to 300 DPI

% Optional: Close the figure after saving
close(gcf);
