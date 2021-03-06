function f = print2D(XF_NAME,YF_NAME,plotName,xl,yl,col)
  xfile_pointer=fopen(XF_NAME, 'r');
  yfile_pointer=fopen(YF_NAME, 'r');
  formatSpec='%f';
  x = fscanf(xfile_pointer,formatSpec);
  y = fscanf(yfile_pointer,formatSpec);
  if yl=="errorRel"
    for i = 1:length(y)
        if y(i)>=1 || y(i)<=-1
            y(i)=1;
        end
        if y(i)<0
            y(i)=-y(i);
        end
    end
  end
  if yl=="errorAbs"
      for i = 1:length(y)
        if y(i)<0
            y(i)=-y(i);
        end
    end
  end
  h=figure;
  plot(x, y, col,'LineWidth', 2);
  xticks([0:2:22])
  grid on;
  title(plotName);
  xlabel(xl);
  ylabel(yl);
  saveas(h,plotName,'jpg');
end
