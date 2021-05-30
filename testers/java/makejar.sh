#!/bin/sh

javac -cp /home/anya/projects/at/uam/jam/lib/*:. javatester/SharedTest.java javatester/CheckStyleTestBase.java
jar cf javatester.jar javatester/SharedTest.class javatester/CheckStyleTestBase.class
