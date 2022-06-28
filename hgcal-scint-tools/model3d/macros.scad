module twinaxAndConnector(twinaxlen=100,pcb_angle=0) {
  rotate([0,0,pcb_angle]) {
  truelen=twinaxlen/cos(pcb_angle);
  // connector
  color("black")
  rotate([0,0,-pcb_angle]) // compensate
  translate([0,0,4/2-0.25]) { cube([2.94,12.6,4],true); }
  // connector pcb
  pcb_height=4-0.25+0.8/2;
  cablespace=1.0;
  connector_pcb_depth=16;
  color("green") {     
    translate([0,0,pcb_height]) { cube([connector_pcb_depth,15.6*2+3*cablespace,0.8],true); }
    translate([3+5+5,0,pcb_height]) { cube([10,2.0+cablespace,0.8],true); }
      translate([3+5+5,0+(-2)*15.6/2-cablespace/2,pcb_height]) { cube([10,2.0,0.8],true); }
      translate([3+5+5,0+(2)*15.6/2+cablespace/2,pcb_height]) { cube([10,2.0,0.8],true); }
  //
  }
  // twin ax
  color("Silver") {
    translate([3+5,0,pcb_height-0.88/2-0.254/2]) {
      rotate([0,90,0]) {
    for (j=[0:1]) {
       for (i=[0:3]) {
        xpos=2.37*i+((i<2)?(0):(3.02))+(2.34+cablespace/2);
        asign=(j==1)?(-1):(1);
        translate([0,asign*xpos,0]) 
           cylinder(truelen,0.88/2,0.88/2,$fn=20);
        translate([0,asign*(xpos+0.79),0]) 
           cylinder(truelen,0.88/2,0.88/2,$fn=20);
       }
       for (i=[0:3]) {
        xpos=0.56*i+(7.52-0.56+cablespace/2);
        asign=(j==1)?(-1):(1);
        translate([0,asign*xpos,0]) 
           cylinder(truelen,0.56/2,0.56/2,$fn=20);
       }
    }
}
      translate([truelen/2,-15.6/2-cablespace/2,0]) {
	cube([truelen,15.6,0.1],true); }
      translate([truelen/2,+15.6/2+cablespace/2,0]) {
	cube([truelen,15.6,0.1],true); }
    }
  }
  }
}
