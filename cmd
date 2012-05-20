#!/bin/bash
rm -f tom.zip && zip -j tom.zip Tales\ of\ Mu/* && ebook-convert tom.zip tom.mobi --output-profile kindle --margin-top 0 --margin-bottom 0 --margin-left 0 --authors="Alexandra Erin" --enable-heuristics
