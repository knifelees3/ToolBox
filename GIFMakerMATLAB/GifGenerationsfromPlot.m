% To generate a gif files from plot

numx=100;
numt=20;
x=linspace(0,6*pi,numx);
t=linspace(0,10,numt);

%% 1. Directly export gif figures needed
%--------------------------------------------------------------
img_series=cell(numt,1);

% Plot for different time
for l=1:numt

    y=sin(x-t(l));
    fig=figure();
    plot(x,y,'r-');
    xlabel('x');ylabel('y');
    drawnow;
    frame = getframe(fig);
    img_series{l,1} = frame2im(frame);
    close(fig);
end

% Export GIF
filename = 'Export_1.gif'; % Specify the output file name
for idx = 1:numt
    [A,map] = rgb2ind(img_series{idx},256);
    if idx == 1
        imwrite(A,map,filename,'gif','LoopCount',Inf,'DelayTime',0.5);
    else
        imwrite(A,map,filename,'gif','WriteMode','append','DelayTime',0.5);
    end
end

%% Export png files and then load and exported into gif
% Create a series if png files
for l=1:numt
    y=sin(x-t(l));
    fig=figure();
    plot(x,y,'r-');
    xlabel('x');ylabel('y');

    % Export PNG
    fig_name=['fig_no_',num2str(l),'.png'];
    print(fig_name,'-dpng');
    close(fig);
end

% Load the png files and then export
delaytime=0.5; % unit is s
exportedGIFName='Export_2.gif';

for l=1:numt
a=imread(['fig_no_',num2str(l),'.png']);

% 因为GIF文件不支持三维数据，所以应调用 rgb2ind，使用颜色图 map 将图像中的 RGB 数据转换为索引图像A
[A, map] = rgb2ind(a,256);
if l==1
   imwrite(A,map,exportedGIFName, 'gif','LoopCount',Inf,'DelayTime',delaytime);
else
   imwrite(A,map,exportedGIFName, 'gif','WriteMode','append','DelayTime',delaytime);
end

end
