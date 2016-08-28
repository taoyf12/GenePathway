% check probability vs. occurrence
clc; clear all; close all;

root = 'G:/GenePathway/pathway_forw_patient/pathway_processed';
path_occr = [root,'/pathway_occr.graph'];
[~,~,~,occr] = textread(path_occr,'%s\t%s\t%s\t%d');
path_prob = [root,'/pathway_prob.graph'];
[~,~,~,prob] = textread(path_prob,'%s\t%s\t%s\t%f');

figure('color',[1 1 1]);
plot(occr, prob,'k.');
hold on;
xlabel('occurrence');
ylabel('sum of probability');
plot([0,6000],[0,6000],'k--')


k = 50;
occr = occr(occr<=k);
prob = prob(prob<=k);
figure('color',[1 1 1]);

subplot(1,2,1);
hist(occr,k);
xlabel('occurrence');
ylabel('frequency');
ylim([0,8e5]);
xlim([0 k]);
subplot(1,2,2);
hist(prob,k);
xlabel('sum\_probability');
ylabel('frequency');
ylim([0,8e5]);


% Q.E.D.
