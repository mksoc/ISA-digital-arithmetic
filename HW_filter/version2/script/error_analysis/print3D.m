function plot3D(XF_NAME,YF_NAME,ZF_NAME,plotName)
  xfile_pointer=fopen(XF_NAME, 'r');
  yfile_pointer=fopen(YF_NAME, 'r');
  zfile_pointer=fopen(ZF_NAME, 'r');
  formatSpec='%f'
  x = fscanf(xfile_pointer,formatSpec);
  y = fscanf(yfile_pointer,formatSpec);
  z = fscanf(zfile_pointer,formatSpec);
% Create bivariate histogram plot using the histogram2 function
  surf(x,y,z);
  xlabel(XF_NAME);
  ylabel(YF_NAME);
  zlabel(ZF_NAME);
  title(plotName);
end
