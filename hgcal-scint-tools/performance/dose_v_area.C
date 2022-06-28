#include "TH2.h"
#include <stdio.h>
#include <set>

std::vector<double> splitter(const char* v);

void dose_v_area(const char* fname) {
  FILE* f=fopen(fname,"r");
  char buffer[1024];

  TCanvas* c1=new TCanvas("c1","c1",700,700);
  c1->SetTopMargin(0.04);
  c1->SetLeftMargin(0.12);
  c1->SetRightMargin(0.04);
  c1->Divide(1,2);
  c1->cd(1);
  TH1* theHisto=new TH1D("hist",";krad;area [m^{2}] per 10 krad",40,0.0,400.0);
  TH1* theHistoI=new TH1D("ihist",";krad;Fraction of area below",40,0.0,400.0);

  theHisto->GetYaxis()->SetTitleOffset(1.0);  
  //  std::vector< std::vector<double> > dataset;
  double min=-1, max=-1;
  double wf;
  const int column=9;
  while (f && !feof(f)) {
    buffer[0]=0;
    fgets(buffer,1000,f);
    if (strchr(buffer,'#')!=0) *(strchr(buffer,'#'))=0;
    std::vector<double> cols=splitter(buffer);
    if (cols.size()<column) continue;
    int binX=cols[0];
    if (binX<=12) wf=720/1.0/(100*100);
    else wf=720/1.25/(100*100);
    
    theHisto->Fill(cols[column],wf*cols[3]);
  }
  theHisto->SetStats(0);

  theHisto->Draw("HIST");

  for (int i=1; i<=40; i++) {
    theHistoI->SetBinContent(i,theHisto->Integral(0,i)/theHisto->Integral());
  }
  c1->cd(2);
  theHistoI->SetStats(0);
  theHistoI->Draw("HIST");
    
  
}
std::vector<double> splitter(const char* v) {
  std::vector<double> rv;
  const char* delim=" \t";
  char* tool=strdup(v);
  for (char* xx=strtok(tool,delim); xx!=0; xx=strtok(0,delim)) {
    rv.push_back(atof(xx));
  }
  free(tool);
  return rv;
}
