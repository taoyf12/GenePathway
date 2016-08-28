% show_roc.m

clc; clear all; close all;
roc1 = load('roc_1e-5.txt');
roc2 = load('roc_3e-5.txt');
roc3 = load('roc_1e-4.txt');

figure('color',[1 1 1]);
hold on;
plot(roc1(:,2),roc1(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc2(:,2),roc2(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');
plot(roc3(:,2),roc3(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','b',...
    'MarkerEdgeColor','k','Color','k');

xlabel('precision')
ylabel('recall');
legend('eps=1e-5','eps=3e-5','eps=1e-4')
%title('')




