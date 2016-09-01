% show.m

clc; clear all; close all;
eps = [1.00E-03
3.00E-04
1.00E-04
3.00E-05
1.00E-05
3.00E-06
1.00E-06
3.00E-07
1.00E-07
3.00E-08];

per_grounded=[49.39467312
65.61743341
70.46004843
74.09200969
75.30266344
76.51331719
76.75544794
76.75544794];

per_pos_grounded=[0.0525697322
0.1948172429
0.2226482776
0.4174655204
0.8132846806
1.895602697
2.622301936
3.246954048
5.723916136
6.936112314];

per_neg_grounded=[0.06178891634
0.1493837919
0.2013591744
0.4103510973
0.7494632088
1.516190968
2.107002047
2.694178485
5.104309686
6.299016557];

per_feature_grounded=[1.409625005
2.855443958
5.512467522
11.14062641
15.52978891
20.71263298
27.47508434
34.40234744
43.0378356
47.20078593];

figure('color',[1 1 1]);
semilogx(eps,per_feature_grounded,'LineWidth',1.5,'Marker','h','MarkerFaceColor','k',...
    'MarkerEdgeColor','k','Color','k');
xlabel('epsilon');
ylabel('percentage of visited features');

ground_time = [2.6
3.3
4.6
6.6
14
37.5
261
747
1011
7132];

figure('color',[1 1 1]);
semilogx(eps,per_pos_grounded,'LineWidth',1.5,'Marker','s','MarkerFaceColor','r',...
    'MarkerEdgeColor','r','Color','r');
hold on;
semilogx(eps,per_neg_grounded,'LineWidth',1.5,'Marker','o','MarkerFaceColor','b');
xlabel('epsilon');
ylabel('percentage grounded');
legend('positive samples','negative samples');

figure('color',[1 1 1]);
loglog(eps,ground_time,'*-');
xlabel('epsilon');
ylabel('ground time/s');

