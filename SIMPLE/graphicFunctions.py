#! /usr/bin/env python
#-*-coding: utf-8 -*-

################################################################################
# GevSeqDev: a tool to generate Release Comparison                              
#
#
#                                                                              
# Arnaud Chiron-Turlay LLR - arnaud.chiron@llr.in2p3.fr                        
#                                                                              
################################################################################

import re
import numpy as np

from sys import argv
argv.append( '-b-' )
import ROOT
ROOT.gROOT.SetBatch(True)
#ROOT.gErrorIgnoreLevel = ROOT.kWarning # remove info like : Info in <TCanvas::Print>: gif file gifs/h_ele_vertexPhi.gif has been created
ROOT.gErrorIgnoreLevel = ROOT.kFatal # ROOT.kBreak # 
argv.remove( '-b-' )

from ROOT import kWhite, kBlue, kBlack, kRed, gStyle, TCanvas, gPad 

class Graphic:
    def __init__(self):
        self.toto = 1.2

    def initRoot(self):
        self.initRootStyle()

    def initRootStyle(self):
        gStyle.SetCanvasBorderMode(1)
        gStyle.SetCanvasColor(kWhite)
        gStyle.SetCanvasDefH(600)
        gStyle.SetCanvasDefW(800)
        gStyle.SetCanvasDefX(0)
        gStyle.SetCanvasDefY(0)
        gStyle.SetPadBorderMode(1)
        gStyle.SetPadColor(kWhite)
        gStyle.SetPadGridX(False)
        gStyle.SetPadGridY(False)
        gStyle.SetGridColor(0)
        gStyle.SetGridStyle(3)
        gStyle.SetGridWidth(1)
        gStyle.SetOptStat(1)
        gStyle.SetPadTickX(1)
        gStyle.SetPadTickY(1)
        gStyle.SetHistLineColor(1)
        gStyle.SetHistLineStyle(0)
        gStyle.SetHistLineWidth(2)
        gStyle.SetEndErrorSize(2)
        gStyle.SetErrorX(0.)
        gStyle.SetTitleColor(1, "XYZ")
        gStyle.SetTitleFont(32, "XYZ")
        gStyle.SetTitleX(0) # ne fonctionne pas avec les gds titres
        gStyle.SetTextAlign(13)
        gStyle.SetTitleX(0);
        gStyle.SetTitleAlign(13);
        gStyle.SetTitleStyle(3002);
        gStyle.SetTitleFillColor(18);
        gStyle.SetTitleXOffset(1.0)
        gStyle.SetTitleYOffset(1.0)
        gStyle.SetLabelOffset(0.005, "XYZ") # numeric label
        gStyle.SetTitleSize(0.05, "XYZ")
        gStyle.SetTitleFont(22,"X")
        gStyle.SetTitleFont(22,"Y")
        gStyle.SetTitleBorderSize(2)
        gStyle.SetPadBottomMargin(0.13) # 0.05
        gStyle.SetPadLeftMargin(0.15)
        gStyle.SetMarkerStyle(21)
        gStyle.SetMarkerSize(0.8)
        gStyle.SetOptTitle(2)
        gStyle.SetPadRightMargin(0.20)
        gStyle.cd()

    def getHisto(self, file, tp):
        #t1 = file.Get("DQMData")
        #t2 = t1.Get("Run 1")
        #t3 = t2.Get("EgammaV")
        #t4 = t3.Get("Run summary")
        #t5 = t4.Get(tp)
        path = 'DQMData/Run 1/EgammaV/Run summary/' + tp
        t_path = file.Get(path)
        return t_path # t5

    def RenderHisto(self, histo):
        if ("ELE_LOGY" in histo.GetOption() and histo.GetMaximum() > 0):
            self.cnv.SetLogy(1)
        histo_name_flag = 1 # use 0 to switch off
        if ( histo.InheritsFrom("TH2") ):
            gStyle.SetPalette(1)
            gStyle.SetOptStat(110+histo_name_flag)
        elif ( histo.InheritsFrom("TProfile") ):
            gStyle.SetOptStat(110+histo_name_flag)
        else: # TH1
            gStyle.SetOptStat(111110+histo_name_flag)

    def PictureChoice(self, histo1, histo2, scaled, err, filename, id):
        if (histo1):
            v_h1 = 1
        else:
            v_h1 = 0
        if (histo2):
            v_h2 = 1
        else:
            v_h2 = 0

        if ( (v_h1 + v_h2) == 0): # no histos at all
            return
        if ( (v_h1 * v_h2) == 0 ): # only one histo
            print('PictureChoice : One histo')
            self.createSinglePicture(histo1, histo2, scaled, err, filename, id, v_h1, v_h2)
        else: # two histos
            if( histo1.InheritsFrom("TH1F") ):
                 print('PictureChoice : TH1F')
                 self.createPicture2(histo1, histo2, scaled, err, filename, id)
            elif ( histo1.InheritsFrom("TProfile") ):
                 print('PictureChoice : TProfile')
                 self.createPicture2(histo1, histo2, scaled, err, filename, id)
            else:
                print('PictureChoice : inherit from nothing')
                self.createPicture(histo1, histo2, scaled, err, filename, id)
            
    def createPicture2(self, histo1, histo2, scaled, err, filename, id):
        new_entries = histo1.GetEntries() # ttl # of bins (9000 in general)
        ref_entries = histo2.GetEntries()
        self.cnv = TCanvas(str(id), "canvas")

        histo2c = histo2.Clone()
        histo3 = histo1.Clone("histo3")
        if ((scaled =="1") and (new_entries != 0) and (ref_entries != 0)):
            rescale_factor = new_entries / ref_entries
            histo2c.Scale(rescale_factor)
        if (histo2c.GetMaximum() > histo1.GetMaximum()):
            histo1.SetMaximum(histo2c.GetMaximum() * 1.1)
        
        self.cnv.SetCanvasSize(960, 900)
        self.cnv.Clear()
        self.cnv.SetFillColor(10)
        self.cnv.SetBorderMode(1)
        
        pad1 = ROOT.TPad(str(id), "pad1", 0, 0.25, 1.0, 1.0) # ,0,0,0
        pad1.SetBottomMargin(0.05)
        pad1.Draw()
        pad1.cd()
        
        if err == "1":
            newDrawOptions ="E1 P"
        else:
            newDrawOptions = "hist"
        
        histo1.SetStats(1)
        histo1.Draw(newDrawOptions) # 
        histo1.SetLineStyle(0)
        histo1.SetLineWidth(2)

        self.RenderHisto(histo1)
        if ("ELE_LOGY" in histo1.GetOption() and histo1.GetMaximum() > 0):
            if (re.search('etaEff_all', filename) or re.search('ptEff_all', filename)):
                print('accord')
                pad1.SetLogy(0)
            else:
                pad1.SetLogy(1)
        gPad.Update()
        
        statBox1 = histo1.GetListOfFunctions().FindObject("stats")
        statBox1.SetTextColor(kRed)
        statBox1.SetBorderSize(2)
        #statBox1.SetFillColor(kGray)
        statBox1.SetFillColorAlpha(18, 0.35) # https://root.cern.ch/doc/master/classTAttFill.html
        statBox1.SetY2NDC(0.995)
        statBox1.SetY1NDC(0.755)
        statBox1.SetX2NDC(0.995)
        statBox1.SetX1NDC(0.795)

        gPad.Update()
        histo2c.Draw("sames hist") # ""  same
        histo2c.SetStats(1)
        self.RenderHisto(histo2c)
        if ("ELE_LOGY" in histo2c.GetOption() and histo2c.GetMaximum() > 0):
            if (re.search('etaEff_all', filename) or re.search('ptEff_all', filename)):
                print('accord')
                pad1.SetLogy(0)
            else:
                pad1.SetLogy(1)
        self.cnv.Update()
        statBox2 = histo2c.GetListOfFunctions().FindObject("stats")
        statBox2.SetTextColor(kBlue)
        y1 = statBox1.GetY1NDC()
        y2 = statBox1.GetY2NDC()
        statBox2.SetY1NDC(2*y1-y2)
        statBox2.SetY2NDC(y1)
        statBox2.SetBorderSize(2)
        statBox2.SetFillColorAlpha(18, 0.35)
        statBox2.SetX2NDC(0.995)
        statBox2.SetX1NDC(0.795)

        newDrawOptions = "sames "
        if err == "1":
            newDrawOptions += "E1 P"
        else:
            newDrawOptions += "hist"
        histo1.Draw(newDrawOptions)
        histo2c.Draw("sames hist")
        
        self.cnv.cd()
        pad2 = ROOT.TPad(str(id), "pad2", 0, 0.05, 1.00, 0.26) # ,0,0,0
        pad2.SetTopMargin(0.025)
        pad2.SetBottomMargin(0.3)
        pad2.SetBorderMode(0)
        pad2.SetGridy()
        pad2.Draw()
        pad2.cd()
        
        #histo3.Divide(histo2) # divide by the original nb of events
        histo3.Divide(histo2c) # divide by the scaled nb of events
        histo3.SetLineColor(kBlack)
        histo3.SetMaximum(2.)
        histo3.SetMinimum(0.)
        histo3.SetStats(0)
        histo3.Sumw2() 
        histo3.SetMarkerStyle(21)
        histo3.Draw("ep")
        
        histo1.SetMarkerColor(kRed)
        histo1.SetLineWidth(3) 
        histo1.SetLineColor(kRed)
        histo1.GetYaxis().SetTitleSize(25)
        histo1.GetYaxis().SetTitleFont(43)
        histo1.GetYaxis().SetTitleOffset(2.00)
        histo1.GetZaxis().SetTitleSize(0.05)
        histo1.SetMarkerStyle(21)
        histo1.SetMarkerSize(0.8)
        
        histo2c.SetLineColor(kBlue)
        histo2c.SetMarkerColor(kBlue)
        histo2c.SetLineWidth(3)
        
        histo3.SetTitle("")
        # Y axis ratio plot settings
        histo3.GetYaxis().SetTitle("ratio h1/h2 ")
        histo3.GetYaxis().SetNdivisions(505)
        histo3.GetYaxis().SetTitleSize(20)
        histo3.GetYaxis().SetTitleFont(43)
        histo3.GetYaxis().SetTitleOffset(1.55)
        histo3.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
        histo3.GetYaxis().SetLabelSize(15)
        # X axis ratio plot settings
        histo3.GetXaxis().SetTitleSize(20)
        histo3.GetXaxis().SetTitleFont(43)
        histo3.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
        histo3.GetXaxis().SetLabelSize(15)

        self.cnv.Draw()
        self.cnv.Update()

        #self.cnv.SaveAs(filename)
        self.cnv.Print(filename)
        self.cnv.Close()
        
        return
            
