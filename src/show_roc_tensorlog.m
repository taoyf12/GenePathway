%% show_roc.m

%% show one
clc; clear all; close all;

n0 = 'proppr_1e-6'; % proppr

% n1 = 'trial001'; % 2 hop, 1 epoch, 0.01 rate, 15 maxdepth, 8 batch
%!1 epoch makes them similar to each other...
% n2 = 'trial002'; % 2 hop, 1 epoch, 0.00000000001 rate, 15 maxdepth, 8 batch
% similar to n3.
% n3 = 'trial003'; % 2 hop, 1 epoch, 0.00 rate, 15 maxdepth, 8 batch
% no training... guess the f are ramdomly set..
% n4 = 'trial004'; % 2 hop, 10 epoch, 0.10 rate, 15 maxdepth, 8 batch
% all precision and recall = 0, 0.10 rate is too large...
n5 = 'trial005'; % 2 hop, 10 epoch, 0.01 rate, 15 maxdepth, 8 batch
% n6 = 'trial006'; % 2 hop, 5 epoch, 0.01 rate, 15 maxdepth, 8 batch
% same with roc5: 5 epoch is enough.
% n7 = 'trial007'; % 2 hop, 2 epoch, 0.01 rate, 15 maxdepth, 8 batch
%!same with n1
% n8 = 'trial008'; % 2 hop, 10 epoch, 0.001 rate, 15 maxdepth, 8 batch
% 0.001 rate is also large enough
n9 = 'trial009'; % 2 hop, 10 epoch, 0.01 rate, 15 maxdepth, 8 batch; no features
% if adding features will not affect result.

% n10 = 'trial010'; % r hop, 10 epoch, 0.01 rate, 15 maxdepth, 8 batch; no features
% 0.0, bug with tensorlog?
n11 = 'trial011'; % 1 hop, 10 epoch, 0.01 rate, 15 maxdepth, 8 batch
n12 = 'trial012'; % 3 hop, 10 epoch, 0.01 rate, 15 maxdepth, 8 batch

roc5 = load(n5);
roc9 = load(n9);
roc11 = load(n12);
roc12 = load(n12);


db.tensorlog.d()



FigHandle = figure('color',[1 1 1]);
hold on;
% plot(roc5(:,3),roc5(:,2),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','r',...
%     'MarkerEdgeColor','k','Color','k');
% plot(roc9(:,3),roc9(:,2),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','g',...
%     'MarkerEdgeColor','k','Color','k');
% plot(roc11(:,3),roc11(:,2),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','b',...
%     'MarkerEdgeColor','k','Color','k');
% plot(roc12(:,3),roc12(:,2),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','y',...
%     'MarkerEdgeColor','k','Color','k');

plot(roc5(:,3),roc5(:,2),'LineWidth',1,'Marker','o', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
% plot(roc9(:,3),roc9(:,2),'LineWidth',1,'Marker','o', 'MarkerFaceColor','g',...
%     'MarkerEdgeColor','k','Color','k');
% plot(roc11(:,3),roc11(:,2),'LineWidth',1,'Marker','o', 'MarkerFaceColor','b',...
%     'MarkerEdgeColor','k','Color','k');
% plot(roc12(:,3),roc12(:,2),'LineWidth',1,'Marker','o', 'MarkerFaceColor','y',...
%     'MarkerEdgeColor','k','Color','k');
ylabel('precision');
xlabel('recall');

legend('2-hop, w/ feature','2-hop, w/o feature','1-hop, w/ feature','3-hop, w/ feature');
%legend('original','order','feature','order+feature');
% title('Effect of rules on ROC')
% 
xlim([0 1]);
ylim([0 1]);
box on;

set(FigHandle, 'Position', [100, 100, 500, 500]);

%%
%A = importdata('betweeness');
clc; close all; clear all;
figure('color',[1 1 1]);
hold on;

fid = fopen('betweenness', 'rt');
C = textscan(fid, '%s\t%f');
fclose(fid);
gene = C{1,1};
betweenness = C{1,2};
bt = (betweenness-min(betweenness))/(max(betweenness)-min(betweenness));

t = 0.01;
xbins = t/2:t:1-t/2;
hist(bt,xbins);
xlabel('normalized betweenness');
ylabel('frequency');

[a,num] = sort(bt);
sel = num((end-9):end);
for i = sel
    fprintf('%s ',gene{i})
end
%xlim([0,0.1])
%ksdensity(bt);
% data_name1 = C{1};
% data_name2 = C{2};
% data_name3 = C{3};



