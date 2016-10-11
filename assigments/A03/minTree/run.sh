#!/bin/sh
ant test
ant jar
java -jar compiler.jar
