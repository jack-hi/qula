#!/usr/bin/python3
# -*- coding: utf-8 -*-


import wx


class CrawlTool(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)

        # url
        url_label = wx.StaticText(self, label="URL: ", size=(100, -1))
        self.url = wx.TextCtrl(self,size=(300, -1))
        url_sizer = wx.BoxSizer(wx.HORIZONTAL)
        url_sizer.Add(url_label, 0, wx.EXPAND)
        url_sizer.Add(self.url, 1, wx.EXPAND)

        # select
        xpath =  wx.StaticText(self, label="xpath: ", size=(100, -1))
        self.select = wx.TextCtrl(self, size=(200, -1))
        self.button = wx.Button(self, label="submit", size=(100, -1))
        self.Bind(wx.EVT_BUTTON, self.on_submit, self.button)
        xpath_sizer = wx.BoxSizer(wx.HORIZONTAL)
        xpath_sizer.Add(xpath, 0, wx.EXPAND)
        xpath_sizer.Add(self.select, 1, wx.EXPAND)
        xpath_sizer.Add(self.button, 0, wx.EXPAND)

        # result
        self.retf = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(url_sizer, 0, wx.EXPAND)
        self.sizer.Add(xpath_sizer, 0, wx.EXPAND)
        self.sizer.Add(self.retf, 1, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show()

    def on_submit(self, event):
        self.retf.write(self.select.GetLineText(0))


app = wx.App(False)

frame = CrawlTool(None, "Crawl Tool")

app.MainLoop()