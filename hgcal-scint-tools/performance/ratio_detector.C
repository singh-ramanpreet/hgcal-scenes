#include "TH2.h"
#include <stdio.h>
#include <set>

std::vector<double> splitter(const char* v);
void set_plot_style(int which);
void draw_additional(int which);

const double zboundaries[]={
  3561.0,3609.0,3657.0,3705.0,3753.0,
  3801.0,3849.0,3890.0,
  3921.3,3969.1,4016.9,4064.7,4122.0,
  4218.8,4305.6,4392.4,4479.2,4566.0,
  4652.8,4739.6,4826.4,4913.2,5000.0,
  5086.8,5172.0,5172.0+85.2};

const int rboundcol=10;

void ratio_detector(const char* fname1, const char* fname2, int column, const char* label, const char* pref=0) {
  char buffer[1024], buffer2[1024];

  TCanvas* c1=new TCanvas("c1","c1",700,700);
  c1->SetTopMargin(0.04);
  c1->SetLeftMargin(0.12);
  c1->SetRightMargin(0.15);
  int istyle=0;
  if (column==8) istyle=2;
  if (column==6) istyle=1;
  set_plot_style(istyle);
  const int offset=350;
  TH2* theHisto=new TH2D("hist",";z [mm];r [mm]",16+8,zboundaries,270-offset/10,offset,2700);

  theHisto->GetYaxis()->SetTitleOffset(1.8);  
  //  std::vector< std::vector<double> > dataset;
  double min=-1, max=-1;
  FILE* f=fopen(fname1,"r");
  FILE* f2=fopen(fname2,"r");
  while (f && !feof(f)) {
    buffer[0]=0;
    fgets(buffer,1000,f);
    fgets(buffer2,1000,f2);
    if (strchr(buffer,'#')!=0) *(strchr(buffer,'#'))=0;
    if (strchr(buffer2,'#')!=0) *(strchr(buffer2,'#'))=0;
    std::vector<double> cols=splitter(buffer);
    std::vector<double> cols2=splitter(buffer2);
    if (cols.size()<column) continue;
    int binX=cols[0];
    int binYa=theHisto->GetYaxis()->FindBin(cols[rboundcol+1]);
    int binYb=theHisto->GetYaxis()->FindBin(cols[rboundcol]);
    for (int binY=binYa;binY<=binYb;binY++) {
      double myval=cols[column]/cols2[column];
      if (min<0 || myval<min) min=myval;
      if (max<myval) max=myval;
      if (theHisto->GetBinContent(binX,binY)>0) {
	myval=(myval+theHisto->GetBinContent(binX,binY))/2;
      } else theHisto->SetBinContent(binX,binY,myval);

    }
    //    dataset.push_back(cols);
  }

  theHisto->SetStats(false);
  if (column==6) {
    theHisto->SetMinimum(min);
    theHisto->SetMaximum(max);
  } else {
    theHisto->SetMinimum(min);
  }

  theHisto->GetZaxis()->CenterTitle(false);

  if (column==4) {
    //    theHisto->SetMaximum(1.0);
    //  theHisto->SetMinimum(0.5);
    c1->SetRightMargin(0.17);
    theHisto->GetZaxis()->SetTitleOffset(1.5);
  }
  
  if (max>100) {
    if (max>1000) {
      theHisto->SetMaximum(1e14);
      theHisto->SetMinimum(3e11);
    }
    c1->SetRightMargin(0.17);
    theHisto->GetZaxis()->SetTitleOffset(1.5);
    //        c1->SetLogz();
  }
  if (min>1000) {
    c1->SetLogz();
  }

  theHisto->Draw("COLZ");
  theHisto->GetZaxis()->SetTitle(label);//"MIP S/N at 3000 fb^{-1}");

  int izleft=(column==6)?(0):(7);
  
  theHisto->GetXaxis()->SetRangeUser(zboundaries[izleft],zboundaries[24]);
  
  TLine* tl=new TLine(zboundaries[izleft],zboundaries[izleft]/sinh(2.4),zboundaries[16+8],zboundaries[16+8]/sinh(2.4));
  tl->SetNDC(false);
  tl->SetLineWidth(3);
  tl->SetLineStyle(kDashed);
  tl->Draw("SAME");

  TLatex* tt=new TLatex(4800,800,"#eta = 2.4");
  tt->Draw("SAME");

//  TLine* tl2=new TLine(zboundaries[0],zboundaries[0]/sinh(2.2),zboundaries[16+8],zboundaries[16+8]/sinh(2.2));
//  tl2->SetNDC(false);
//  tl2->SetLineWidth(3);
//  tl2->SetLineStyle(kDashed);
//  tl2->Draw("SAME");
//
//  TLatex* tt2=new TLatex(4800,1000,"#eta = 2.2");
//  tt2->Draw("SAME");


  TLine* tl3=new TLine(zboundaries[izleft],zboundaries[izleft]/sinh(3.0),zboundaries[16+8],zboundaries[16+8]/sinh(3.0));
  tl3->SetNDC(false);
  tl3->SetLineWidth(3);
  //  tl2->SetLineStyle(kDashed);
  tl3->Draw("SAME");

  TLatex* tt3=new TLatex(4800,530,"#eta = 3.0");
  tt3->Draw("SAME");

  draw_additional(0);
  if (column==5 || column==7) draw_additional(1);

  //TLatex* tt4=new TLatex(3600,2400,"Scenario 5 + 15%");
  if (column==6) {
    //TLatex* tt4=new TLatex(3600,2400,"D=3.5 #sqrt{R} (Best 10 HPD fit)");
    TLatex* tt4=new TLatex(3600,2400,"D=6.0 R^{0.35} (Tile-only fit)");
    tt4->SetTextSize(0.03);
    tt4->Draw("SAME");
    TLatex* tt5=new TLatex(3600,2300,"12.3 PE/MIP (Reduced SiPM PDE)");
    //TLatex* tt5=new TLatex(3600,2300,"18 PE/MIP (ESR)");
    tt5->SetTextSize(0.03);
    tt5->Draw("SAME");
  }
  TLatex* tt6=new TLatex(0.126,0.967,"CMS");
  tt6->SetNDC(1);
  tt6->SetTextSize(0.03);
  tt6->Draw("SAME");
  
  char name[100];

  if (pref!=0) {
    //    sprintf(name,"%s.jpg",pref); c1->Print(name);
    sprintf(name,"%s.png",pref); c1->Print(name);
    sprintf(name,"%s.pdf",pref); c1->Print(name);
  }
  
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

void drawX(int what, double x1, double y1, double x2, double y2) {
  TLine* tl=new TLine(x1,y1,x2,y2);
  tl->SetNDC(false);
  if (what==0) {
    tl->SetLineWidth(3);  
    tl->SetLineColor(kBlue);
  } else if (what==1) {
    tl->SetLineWidth(2);  
    tl->SetLineColor(kBlack);
    tl->SetLineStyle(kDashed);
  }
  tl->Draw("SAME");
}

void draw_additional(int what) {
  if (what==0) { // scintillator/silicon boundary 
    drawX(what,zboundaries[14+8],902,zboundaries[16+8],902);
    drawX(what,zboundaries[14+8],902,zboundaries[14+8],902);
    drawX(what,zboundaries[7+8],902,zboundaries[14+8],902);
    drawX(what,zboundaries[7+8],902,zboundaries[7+8],902);
    drawX(what,zboundaries[7+8],902,zboundaries[6+8],902);
    drawX(what,zboundaries[6+8],902,zboundaries[6+8],1051);
    drawX(what,zboundaries[6+8],1051,zboundaries[5+8],1051);
    drawX(what,zboundaries[5+8],1051,zboundaries[5+8],1147);
    drawX(what,zboundaries[5+8],1147,zboundaries[4+8],1147);  
    drawX(what,zboundaries[4+8],1147,zboundaries[4+8],1190);
    drawX(what,zboundaries[4+8],1190,zboundaries[3+8],1190);
    drawX(what,zboundaries[3+8],1190,zboundaries[3+8],1190);  
    drawX(what,zboundaries[3+8],1190,zboundaries[2+8],1190);    
    drawX(what,zboundaries[2+8],1190,zboundaries[2+8],1304);
    drawX(what,zboundaries[2+8],1304,zboundaries[1+8],1304);
    drawX(what,zboundaries[1+8],1304,zboundaries[1+8],1365);
    drawX(what,zboundaries[1+8],1365,zboundaries[0+8],1365);
    drawX(what,zboundaries[0+8],1365,zboundaries[0+8],1915);
  } else {
    //    drawX(what,zboundaries[14+8],902,zboundaries[16+8],902);
    //drawX(what,zboundaries[14+8],902,zboundaries[14+8],902);
    //drawX(what,zboundaries[7+8],902,zboundaries[14+8],902);
    drawX(what,zboundaries[7+8],902,zboundaries[7+8],1006);
    drawX(what,zboundaries[7+8],1006,zboundaries[6+8],1006);
    drawX(what,zboundaries[6+8],1006,zboundaries[6+8],1122);
    drawX(what,zboundaries[6+8],1122,zboundaries[5+8],1122);
    drawX(what,zboundaries[5+8],1122,zboundaries[5+8],1279);
    drawX(what,zboundaries[5+8],1279,zboundaries[4+8],1279);  
    drawX(what,zboundaries[4+8],1279,zboundaries[4+8],1265);
    drawX(what,zboundaries[4+8],1265,zboundaries[3+8],1265);
    drawX(what,zboundaries[3+8],1265,zboundaries[3+8],1327);  
    drawX(what,zboundaries[3+8],1327,zboundaries[2+8],1327);    
    drawX(what,zboundaries[2+8],1327,zboundaries[2+8],1399);
    drawX(what,zboundaries[2+8],1399,zboundaries[1+8],1399);
    drawX(what,zboundaries[1+8],1399,zboundaries[1+8],1448);
    drawX(what,zboundaries[1+8],1448,zboundaries[0+8],1448);
    drawX(what,zboundaries[0+8],1448,zboundaries[0+8],1915);    
  }
}

void
set_plot_style(int which)
{
  if (which == 1 ) {
    
    const Int_t NRGBs = 7;
    const Int_t NCont = 100;

    Double_t stops[NRGBs] = { 0.00, 0.25, 0.35, 0.55, 0.63, 0.75, 1.00 };
    Double_t red[NRGBs]   = { 0.51, 1.00, 0.87, 0.00, 0.0, 0.00, 0.0 };
    Double_t green[NRGBs] = { 0.00, 0.20, 1.0, 1.0, 1.00, 1.00, 0.20 };
    Double_t blue[NRGBs]  = { 0.00, 0.00, 0.12, 0.0, 0.6, 1.00, 0.51 };
    TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
    gStyle->SetNumberContours(NCont);
  } else if (which==2) {
    const Int_t NRGBs = 7;
    const Int_t NCont = 100;

    Double_t stops[NRGBs] = { 0.00, 0.20, 0.40, 0.60, 0.75, 0.90, 1.00 };
    Double_t red[NRGBs]   = { 0.00, 0.00, 0.0, 0.00, 0.87, 1.00, 0.51 };
    Double_t green[NRGBs] = { 0.20, 1.00, 1.0, 1.0, 1.00, 0.20, 0.00 };
    Double_t blue[NRGBs]  = { 0.51, 1.00, 0.6, 0.0, 0.12, 0.00, 0.00 };
    TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
    gStyle->SetNumberContours(NCont);
  } else {
    const Int_t NRGBs = 7;
    const Int_t NCont = 100;

    Double_t stops[NRGBs] = { 0.00, 0.125, 0.225, 0.25, 0.41, 0.60, 1.00 };
    Double_t red[NRGBs]   = { 0.00, 0.00, 0.0, 0.00, 0.87, 1.00, 0.51 };
    Double_t green[NRGBs] = { 0.20, 1.00, 1.0, 1.0, 1.00, 0.20, 0.00 };
    Double_t blue[NRGBs]  = { 0.51, 1.00, 0.6, 0.0, 0.12, 0.00, 0.00 };
    TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
    gStyle->SetNumberContours(NCont);
  }
}
