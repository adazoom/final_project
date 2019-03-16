%% pupil detection
close all;
clear all;
I = im2double(imread('front_raw.png'));
grayImage = rgb2gray(I);
f = fastRadialSymmetryTransform(grayImage, 100, 2, 0.01);
level = graythresh(f);
binaryMask= im2bw(f,level);
binaryMaskNew = binaryMask;
CC = bwconncomp(binaryMaskNew);
numPixels = cellfun(@numel,CC.PixelIdxList);
[connComps,idx] = sort(numPixels,'descend');
binaryMask(CC.PixelIdxList{idx(1)}) = 0;
filteredImage = imsubtract(binaryMaskNew,binaryMask);
[labels, num] = bwlabel(filteredImage);

figure, imshow(grayImage), title('Probable Pupil Locations'), hold on,
s = regionprops(labels, 'BoundingBox', 'Area', 'Centroid','MajorAxisLength','MinorAxisLength');
rectangle('position', s(1).BoundingBox,'EdgeColor','b','linewidth',2); hold on;

% pupil centroid
pupilCenters(1,1) = s(1).Centroid(1);
pupilCenters(1,2) = s(1).Centroid(2);

cx = pupilCenters(1,1);
cy = pupilCenters(1,2);
[height, width] = size(grayImage);
pupilArea_upperleft = max(0, cy - 120);
pupilArea_lowerleft = min(cy + 120, height);
pupilArea_upperright =  max(0, cx - 120);
pupilArea_lowerright = min(cx + 120, width);
pupilArea = grayImage(pupilArea_upperleft:pupilArea_lowerleft, pupilArea_upperright: pupilArea_lowerright);
% figure; imshow(pupilArea);
level = graythresh(pupilArea);
pupilArea_BW = im2bw(pupilArea,level);
% figure; imshow(pupilArea_BW);
SE = strel('diamond', 3);
pupilArea_BWdilate = imdilate(pupilArea_BW, SE);
pupil_edge = pupilArea_BWdilate - pupilArea_BW;

[x,y] = find(pupil_edge == 1);
x = x + pupilArea_upperright;
y = y + pupilArea_upperleft;
plot(x,y,'o');


% TODO: calculate most close fitting ellipse
% [y, x] = find(pupilArea_BWdilate == 1);  
% xy = [x, y];
% ellipse_params = EllipseDirectFit(xy);
% contour_params = CalculateEllipse(ellipse_params);
