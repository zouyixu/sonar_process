rows = 401;
cols = 512;
dr = 0.02;
FOV = 80;

%% 1. 读取文件
fid = fopen('frame.dat', 'rb');
if fid == -1
    error('无法打开文件 frame.dat');
end

data = fread(fid, rows*cols, 'uint8=>uint8');
fclose(fid);

% MATLAB 按列填充
data = reshape(data, [cols, rows])';
data_filtered = medfilt2(data);

% figure;
% imagesc(data);
% colormap(gray(256));

% axis image;     %tick inside

% colorbar;   %colorbar beside

% title('极坐标/声呐数据');
% xlabel('列');
% ylabel('行');

%% 2. 构造极坐标网格并且转化为直角坐标
r  = (0:rows-1) * dr;

theta = deg2rad(linspace(-FOV/2, FOV/2, cols));

[R, Theta] = ndgrid(r, theta);        % R(i,j)=r(i)，Theta(i,j)=theta(j)

[X, Y] = pol2cart(Theta, R);

%% 3. 绘制扇形图
figure(2);
p = pcolor(Y, X, data_filtered);
p.EdgeColor = 'none';
% shading interp;
% axis equal;
colormap(gray(256));

colorbar;

xlabel('X (m)');
ylabel('Y (m)');
title('filtered');

figure(3);
p = pcolor(Y, X, data);
p.EdgeColor = 'none';
% shading interp;
% axis equal;
colormap(gray(256));
title('unfiltered')