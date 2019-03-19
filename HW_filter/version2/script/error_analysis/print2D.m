function f = print2D(XF_NAME,YF_NAME,plotName)
  xfile_pointer=fopen(XF_NAME, 'r');
  yfile_pointer=fopen(YF_NAME, 'r');
  formatSpec='%f';
  x = fscanf(xfile_pointer,formatSpec);
  y = fscanf(yfile_pointer,formatSpec);
  h=figure;
  plot(x, y, 'b','LineWidth', 2);
  grid on;
  %axis([0 length(x) 0 length(y)]);
  title(plotName);
  %xlabel("X");
  %ylabel("Y");
  saveas(h,plotName,'jpg');
end
