## Desktop-Fountain-Base-Generator
Python Macro for FreeCAD to create custom bases for the Modular Desktop Fountain Project.

This python script is intended to be used as a macro in FreeCAD.

The script can be used to create custom bases for the "Modular Desktop Fountain" by "3D Printy". 
The Modular Desktop Fountain can be found on Printables: https://www.printables.com/model/239774-modular-desktop-fountain

**__Recomended use for testing various shapes:__**
  <ul>
  <li>Install FreeCAD
  <li>Download the python script from this repository 
  <li>Add the file to your FreeCAD macro folder 
    <ul>
    <li>If you don't know the location of the folder, you can find it in FreeCAD: "Macro" --> "Macros" --> "User macros location" 
    <li>You can also copy the contents of the file and create a new macro in FreeCAD and paste the contents 
    </ul>
  <li>Open the file (which is already stored in the macro folder) with a texteditor like Atom, Notepad or Notepad++
   <li>Open FreeCAD --> open a new file --> "Macro" --> "Macros" --> select the macro --> macro should be executed
  <li>After you executed the macro once, you can find it under "Macro" --> "Recent macros", whith its Shortcut (something like Ctrl + Shift + 1)
   <li>Go into the texteditor (macro file is already open) and change the parameters 
   <li>Save the changes in the texteditor (usually "Ctrl + S" should work)
   <li>Go into FreeCAD and press the keystroke for the recently used macro (usually "Ctrl + Shift + 1")
   <li>This should allow to quickly test various parameters (especially if you have two monitors)
   <li>There might be a better way, but thats the way I wrote and debugged the script
   
   <li>Befor you wan't to export the created object, don't forget to add chamfers (if you want them):
     <ul>
       <li>this has to be done by hand in FreeCAD
       <li>switch to "Part" workbench
       <li>click on the "FinalBase_Refined" (body which is displayed) in the treeView of FreeCAD
       <li>select "Part" --> "Chamfer"
       <li>toggle "Select faces"
       <li>click on the following faces: bottom of the base, bottom of the rim, bottom on the inside
       <li>click "Ok" --> this might take some time
     </ul>
     
   <li>the shape can be customized by changing the values of arrange
   <li>a '1' in arange is used to create a hexagon, a '0' is used to create a empty space
   <li>you can also choose some presets, which can be found at the begining of the code
   </ul>

 Pay Attention to the following:
 <ul>
  <li>if you exectue the macro again after you added chamfers, you will have to add them again
  <li>if you want to use the original baseplates, don't change the wall thickness
  <li>inspect if all features are located correctly before printing
  
   
   
   
   
