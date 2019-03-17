function f = print2D(XF_NAME,YF_NAME)

  xfile_pointer=fopen(XF_NAME, 'r');
  yfile_pointer=fopen(YF_NAME, 'r');
  formatSpec='%f';
  x = fscanf(xfile_pointer,formatSpec);
  y = fscanf(xfile_pointer,formatSpec);

  % Plot y1 vs. x (blue, solid) and y2 vs. x (red, dashed)
  figure
  plot(x, y1, 'b', x, y2, 'r-.', 'LineWidth', 2)

  % Turn on the grid
  grid on

  % Set the axis limits
  axis([0 2*pi -1.5 1.5])

  % Add title and axis labels
  title('Trigonometric Functions')
  xlabel('angle')
  ylabel('sin(x) and cos(x)')
end
