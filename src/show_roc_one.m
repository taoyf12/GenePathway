% show_roc.m

% Comparison of parameters.
clc; clear all; close all;

n1 = 'eps=1e-4';
n2 = 'eps=1e-5';
n3 = 'eps=1e-6';
n4 = 'eps=1e-7';
n5 = 'alph=0.05';
roc1 = load(n1);
roc2 = load(n2);
roc3 = load(n3);
roc4 = load(n4);
roc5 = load(n5);
figure('color',[1 1 1]);
hold on;
plot(roc1(:,2),roc1(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','k',...
    'MarkerEdgeColor','k','Color','k');
plot(roc2(:,2),roc2(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc3(:,2),roc3(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');
plot(roc4(:,2),roc4(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','b',...
    'MarkerEdgeColor','k','Color','k');
plot(roc5(:,2),roc5(:,3),'LineWidth',1.5,'Marker','s', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
xlabel('precision');
ylabel('recall');
legend(n1,n2,n3,n4,n5);
%title('')
% 
xlim([0 1])
ylim([0 1])
box on
%%
% Comparison of weighted and unweight edges.

clc; clear all; close all;

n1 = 'eps=1e-4';
n2 = 'w=1.0,eps=1e-4';
n3 = 'eps=1e-7';
n4 = 'w=1.0,eps=1e-7';
% n5 = 'alph=0.05';
roc1 = load(n1);
roc2 = load(n2);
roc3 = load(n3);
roc4 = load(n4);

figure('color',[1 1 1]);
hold on;
plot(roc1(:,2),roc1(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc2(:,2),roc2(:,3),'LineWidth',1.5,'Marker','s', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc3(:,2),roc3(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');
plot(roc4(:,2),roc4(:,3),'LineWidth',1.5,'Marker','s', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');

xlabel('precision');
ylabel('recall');
legend(n1,n2,n3,n4);
%title('')
% 
xlim([0 1])
ylim([0 1])
box on

%%
% Comparison of 10% and 90% patients.
% sga2deg,sga,deg
% 1418704 9812 5776
% 0.948250417077 0.998270424255 1.0
% clc; clear all; close all;

n1 = 'eps=1e-7';
n2 = '90,eps=1e-6';

% n5 = 'alph=0.05';
roc1 = load(n1);
roc2 = load(n2);

figure('color',[1 1 1]);
hold on;
plot(roc1(:,2),roc1(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc2(:,2),roc2(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');


xlabel('precision');
ylabel('recall');
legend('based on 10% patients','based on 90% patients');
%title('')
% 
xlim([0 1])
ylim([0 1])
box on

%%
% Effect of training
% sga2deg_train	sga2deg_test	sga2deg_remain
% 362439	369037	1328929
% 		149683	276458
% sga_train	sga_test	sga_remain
% 8396	8453	9786
% 		7659	8372
% deg_train	deg_test	deg_remain
% 5730	5711	5776
% 		5679	5730

%  INFO [Grounder] Total items: 8396
%  INFO [Grounder] Grounded: 8371
%  INFO [Grounder] Skipped: 25 = 25 with no labeled solutions; 0 with empty graphs
%  INFO [Grounder] totalPos: 362439 totalNeg: 47746641 coveredPos: 191739 coveredNeg: 844435
%  INFO [Grounder] For positive examples 191739/362439 proveable [52.90241944161638%]
%  INFO [Grounder] For negative examples 844435/47746641 proveable [1.7685746731377396%]
%  INFO [Grounder] Example with fewest [0.0%] pos examples covered: pathTo(scn2a,X1).
% Grounding time: 198511


clc; clear all; close all;

n1 = 'train,untrained,eps=1e-4';
n2 = 'test,untrained,eps=1e-4';
n3 = 'train,trained,eps=1e-4';
n4 = 'test,trained,eps=1e-4';
n5 = 'train,untrained1,eps=1e-4';
n6 = 'test,untrained1,eps=1e-4';
nn = 'justtrain1'
% n5 = 'alph=0.05';
roc1 = load(n1);
roc2 = load(n2);
roc3 = load(n3);
roc4 = load(n4);
roc5 = load(n5);
roc6 = load(n6);

rocn = load(nn);

figure('color',[1 1 1]);
hold on;
% recall = 0.208
plot(roc1(:,2),roc1(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc2(:,2),roc2(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');
plot(roc3(:,2),roc3(:,3),'LineWidth',1.5,'Marker','s', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc4(:,2),roc4(:,3),'LineWidth',1.5,'Marker','s', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');
plot(roc5(:,2),roc5(:,3),'LineWidth',1.5,'Marker','d', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc6(:,2),roc6(:,3),'LineWidth',1.5,'Marker','d', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');


plot(rocn(:,2),rocn(:,3),'LineWidth',1.5,'Marker','d', 'MarkerFaceColor','y',...
    'MarkerEdgeColor','k','Color','k');

xlabel('precision');
ylabel('recall');
legend('train,untrained','test,untrained','train,trained','test,trained',...
    'train,untrained1','test,untrained1');
%legend('based on 10% patients','based on 90% patients');
%title('')
% 
xlim([0 1])
ylim([0 1])
box on


%%
% Test on the ones edge and weighted edges.


clc; clear all; close all;

n1 = 'train,untrained,eps=1e-4';
n2 = 'test,untrained,eps=1e-4';
n3 = 'train,trained1,eps=1e-4';
n4 = 'test,trained,eps=1e-4';
% n5 = 'alph=0.05';
roc1 = load(n1);
roc2 = load(n2);
roc3 = load(n3);
roc4 = load(n4);

figure('color',[1 1 1]);
hold on;
% recall = 0.208
plot(roc1(:,2),roc1(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc2(:,2),roc2(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');
plot(roc3(:,2),roc3(:,3),'LineWidth',1.5,'Marker','s', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc4(:,2),roc4(:,3),'LineWidth',1.5,'Marker','s', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');

xlabel('precision');
ylabel('recall');
legend('train,untrained','test,untrained','train,trained','test,trained');
%legend('based on 10% patients','based on 90% patients');
%title('')
% 
xlim([0 1])
ylim([0 1])
box on

%%
%% Show the baseline of untrained test dataset.
% fig1
clc; clear all; close all;


n1 = 'test,untrained,eps=1e-4';
n2 = 'test,untrained,eps=1e-5';
n3 = 'test,untrained,alph=0.05';
roc1 = load(n1);
roc2 = load(n2);
roc3 = load(n3);

figure('color',[1 1 1]);
hold on;
% recall = 0.208
plot(roc1(:,2),roc1(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc2(:,2),roc2(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');
plot(roc3(:,2),roc3(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','b',...
    'MarkerEdgeColor','k','Color','k');
% plot(roc4(:,2),roc4(:,3),'LineWidth',1.5,'Marker','s', 'MarkerFaceColor','g',...
%     'MarkerEdgeColor','k','Color','k');

xlabel('precision');
ylabel('recall');
% legend('train,untrained','test,untrained','train,trained','test,trained');
%legend('based on 10% patients','based on 90% patients');
legend('eps=1e-4:alph=0.1','eps=1e-5:alph=0.1','eps=1e-4:alph=0.05')
title('ROC of test set w/o training');

xlim([0 1])
ylim([0 1])
box on

%%


% fig2

clc; clear all; close all;


n1 = 'test,untrained,eps=1e-4';
n2 = 'test,untrained,edge=1';
n3 = 'test,untrained,edge=2';
n4 = 'test,untrained,edge=3';
n5 = 'test,untrained,edge=h';

roc1 = load(n1);
roc2 = load(n2);
roc3 = load(n3);
roc4 = load(n4);
roc5 = load(n5);
figure('color',[1 1 1]);
hold on;
% recall = 0.208
plot(roc1(:,2),roc1(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc2(:,2),roc2(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');
plot(roc3(:,2),roc3(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','b',...
    'MarkerEdgeColor','k','Color','k');
% plot(roc4(:,2),roc4(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','y',...
%     'MarkerEdgeColor','k','Color','k');
plot(roc5(:,2),roc5(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','y',...
    'MarkerEdgeColor','k','Color','k');

xlabel('precision');
ylabel('recall');
% legend('train,untrained','test,untrained','train,trained','test,trained');
%legend('based on 10% patients','based on 90% patients');
legend('wt_{edge}= sum of prob','wt_{edge}=1.0','wt_{edge}=wt_{edge}^2',...
    'wt_{edge}=sqrt(wt_{edge})');
% legend('wt_{edge}= sum of prob','wt_{edge}=1.0','wt_{edge}=wt_{edge}^2',...
%     'wt_{edge}=wt_{edge}^3','wt_{edge}=sqrt(wt_{edge})');
title('effect of external edge weight');

xlim([0 1])
ylim([0 1])
box on

%%

% fig3


clc; clear all; close all;


n1 = 'test,untrained,eps=1e-4';
n2 = 'test,untrained,unorm';

roc1 = load(n1);
roc2 = load(n2);
figure('color',[1 1 1]);
hold on;
% recall = 0.208
plot(roc1(:,2),roc1(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc2(:,2),roc2(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');

xlabel('precision');
ylabel('recall');
% legend('train,untrained','test,untrained','train,trained','test,trained');
%legend('based on 10% patients','based on 90% patients');
legend();

xlim([0 1])
ylim([0 1])
box on


%%

% fig4

clc; clear all; close all;


n1 = 'test,untrained,eps=1e-4';
n2 = 'test,untrained,eps=1e-4r';

roc1 = load(n1);
roc2 = load(n2);
figure('color',[1 1 1]);
hold on;
% recall = 0.208
plot(roc1(:,2),roc1(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc2(:,2),roc2(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');

xlabel('precision');
ylabel('recall');
% legend('train,untrained','test,untrained','train,trained','test,trained');
%legend('based on 10% patients','based on 90% patients');
legend();

xlim([0 1])
ylim([0 1])
box on

%%

% 'test,trained,eps=1e-4'
% fig5

clc; clear all; close all;


n1 = 'test,untrained,eps=1e-4';
n2 = 'test,trained,eps=1e-4';

roc1 = load(n1);
roc2 = load(n2);
figure('color',[1 1 1]);
hold on;
% recall = 0.208
plot(roc1(:,2),roc1(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc2(:,2),roc2(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');

xlabel('precision');
ylabel('recall');
% legend('train,untrained','test,untrained','train,trained','test,trained');
legend('untrained','trained');
title('effect of training');

xlim([0 1])
ylim([0 1])
box on

%%

% 10%
% sga2deg,sga,deg
% 362439 8396 5730
% 0.242251331437 0.854206938651 0.99203601108


% fig6
% sga2deg,sga,deg
% 1418704 9812 5776
% 0.948250417077 0.998270424255 1.0
% clc; clear all; close all;



n1 = '10,eps=1e-6';
n2 = '20,eps=1e-6';
n3 = '90,eps=1e-6';
% n5 = 'alph=0.05';
roc1 = load(n1);
roc2 = load(n2);
roc3 = load(n3);
figure('color',[1 1 1]);
hold on;
plot(roc1(:,2),roc1(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','r',...
    'MarkerEdgeColor','k','Color','k');
plot(roc2(:,2),roc2(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','g',...
    'MarkerEdgeColor','k','Color','k');
plot(roc3(:,2),roc3(:,3),'LineWidth',1.5,'Marker','o', 'MarkerFaceColor','b',...
    'MarkerEdgeColor','k','Color','k');

xlabel('precision');
ylabel('recall');
legend('based on 10% patients','based on 20% patients','based on 90% patients');
title('ROC of constructed graph')
% 
xlim([0 1])
ylim([0 1])
box on




















