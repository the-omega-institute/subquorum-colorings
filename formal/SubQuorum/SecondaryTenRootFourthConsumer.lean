import Lean.Elab.Tactic.Omega

set_option autoImplicit false

namespace SubQuorum.SecondaryTenRootFourthConsumer

abbrev Point := Int × Int

def endpoint (breadth near far : Int) (point : Point) : Prop :=
  ((point.1 = 0 ∨ point.1 = 1) ∧ 1 ≤ point.2 ∧ point.2 ≤ breadth) ∨
  (2 ≤ point.1 ∧ point.1 ≤ near ∧ point.2 = 1) ∨
  (2 ≤ point.1 ∧ point.1 ≤ far ∧ point.2 = breadth)

def fourth (origin offset oldWidth height incident far : Int) (down : Bool)
    (point : Point) : Prop :=
  endpoint height incident far
    (point.2-offset-oldWidth-12+incident,
     if down then point.1-origin+10 else origin-8-point.1)

def parent (origin offset oldWidth width depth : Int) (point : Point) : Prop :=
  endpoint (oldWidth+width+26) (depth+4) 4
    (point.1-origin+14,point.2-offset+width+13)

def consumer (origin offset breadth far : Int) (point : Point) : Prop :=
  endpoint breadth 4 far (point.1-origin+8,offset+1-point.2)

def oldP (origin offset oldWidth : Int) (point : Point) : Prop :=
  endpoint (oldWidth+12) 10 4 (point.1-origin+8,offset+oldWidth+13-point.2)

def nextP (origin offset width depth : Int) (point : Point) : Prop :=
  endpoint (width+12) 10 4 (point.1-origin-depth+14,offset+1-point.2)

def oldX (origin offset : Int) (point : Point) : Prop :=
  endpoint 6 4 4 (origin+2-point.1,offset+2-point.2)

def oldV (origin offset oldWidth depth : Int) (point : Point) : Prop :=
  endpoint (oldWidth+10) 8 depth (point.1-origin+6,offset+oldWidth+12-point.2)

theorem incident_crosses_parent (origin offset oldWidth width depth height incident far : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) (hdepth : 24 ≤ depth)
    (hheight : 6 ≤ height) (hlong : oldWidth+width+24 ≤ incident) (down : Bool) :
    fourth origin offset oldWidth height incident far down (origin-9,offset-width-12) ∧
    parent origin offset oldWidth width depth (origin-9,offset-width-12) := by
  cases down <;> unfold fourth parent endpoint <;> dsimp <;> omega

theorem upward_bar_hits_parent (origin offset oldWidth width depth height incident far : Int)
    (hheight : 6 ≤ height)
    (hincident : 4 ≤ incident) (hshort : incident ≤ oldWidth+width+22) :
    fourth origin offset oldWidth height incident far false
      (origin-13,offset+oldWidth+12-incident) ∧
    parent origin offset oldWidth width depth
      (origin-13,offset+oldWidth+12-incident) := by
  unfold fourth parent endpoint
  dsimp
  omega

theorem short_incident_hits_old_bars
    (origin offset oldWidth breadth consumerFar height incident far : Int)
    (hold : 12 ≤ oldWidth) (hheight : 6 ≤ height)
    (hincident : 4 ≤ incident) (hshort : incident ≤ oldWidth+breadth+12) :
    fourth origin offset oldWidth height incident far true
      (origin-8,offset+oldWidth+13-incident) ∧
    (consumer origin offset breadth consumerFar
      (origin-8,offset+oldWidth+13-incident) ∨
     oldP origin offset oldWidth (origin-8,offset+oldWidth+13-incident)) := by
  unfold fourth consumer oldP endpoint
  dsimp
  omega

theorem tall_bar_hits_nextP (origin offset oldWidth width depth breadth height incident far : Int)
    (hold : 12 ≤ oldWidth) (hdepth : 24 ≤ depth)
    (hbreadth : 6 ≤ breadth) (hlower : oldWidth+breadth+14 ≤ incident)
    (hupper : incident ≤ oldWidth+width+22) (htall : depth-4 ≤ height) :
    fourth origin offset oldWidth height incident far true
      (origin+depth-14,offset+oldWidth+12-incident) ∧
    nextP origin offset width depth
      (origin+depth-14,offset+oldWidth+12-incident) := by
  unfold fourth nextP endpoint
  dsimp
  omega

theorem far_hits_consumer (origin offset oldWidth breadth consumerFar height incident far : Int)
    (hheight : 6 ≤ height) (hnear : height ≤ consumerFar+2)
    (hlower : oldWidth+breadth+14 ≤ incident)
    (hfar : incident-oldWidth-breadth-11 ≤ far) :
    fourth origin offset oldWidth height incident far true
      (origin+height-10,offset+1-breadth) ∧
    consumer origin offset breadth consumerFar (origin+height-10,offset+1-breadth) := by
  unfold fourth consumer endpoint
  dsimp
  omega

theorem far_hits_oldX (origin offset oldWidth breadth height incident far : Int)
    (hbreadth : 6 ≤ breadth) (hheight : 8 ≤ height ∧ height ≤ 12)
    (hlower : oldWidth+breadth+14 ≤ incident) (hfar : incident-oldWidth-16 ≤ far) :
    fourth origin offset oldWidth height incident far true (origin+height-10,offset-4) ∧
    oldX origin offset (origin+height-10,offset-4) := by
  unfold fourth oldX endpoint
  dsimp
  omega

theorem far_hits_oldV (origin offset oldWidth depth breadth height incident far : Int)
    (hbreadth : 6 ≤ breadth)
    (hheight : 14 ≤ height ∧ height ≤ depth-6)
    (hlower : oldWidth+breadth+14 ≤ incident) (hfar : incident-oldWidth-10 ≤ far) :
    fourth origin offset oldWidth height incident far true (origin+height-10,offset+2) ∧
    oldV origin offset oldWidth depth (origin+height-10,offset+2) := by
  unfold fourth oldV endpoint
  dsimp
  omega

theorem even_bounds (oldWidth width breadth depth height incident : Int)
    (hincident : incident % 2 = 0) (hheight : height % 2 = 0)
    (hold : oldWidth % 2 = 0) (hwidth : width % 2 = 0)
    (hbreadth : breadth % 2 = 0) (hdepth : depth % 2 = 0)
    (hsmall : ¬incident ≤ oldWidth+breadth+12)
    (hlarge : ¬oldWidth+width+24 ≤ incident) (htall : ¬depth-4 ≤ height) :
    oldWidth+breadth+14 ≤ incident ∧ incident ≤ oldWidth+width+22 ∧ height ≤ depth-6 := by
  omega

theorem existence_frontier (oldWidth width depth breadth consumerFar height incident far : Int)
    (hlower : oldWidth+breadth+14 ≤ incident) (hupper : incident ≤ oldWidth+width+22)
    (hheight : height ≤ depth-6) (hfar : 4 ≤ far)
    (hwidth : width % 2 = 0) (hbreadth : breadth % 2 = 0)
    (hheightEven : height % 2 = 0) (hconsumerEven : consumerFar % 2 = 0)
    (hcap : height ≤ consumerFar+2 → far ≤ incident-oldWidth-breadth-12) :
    breadth ≤ width+6 ∨ (breadth = width+8 ∧ consumerFar ≤ depth-10) := by
  omega

theorem short_witness (oldWidth width depth breadth consumerFar : Int)
    (hdepth : 24 ≤ depth) (hbreadth : breadth ≤ width+6)
    (hconsumer : 4 ≤ consumerFar) :
    oldWidth+breadth+14 ≤ oldWidth+width+22 ∧ 6 ≤ depth-6 ∧
    6 ≤ consumerFar+2 ∧ 4 ≤ (oldWidth+width+22)-oldWidth-breadth-12 := by
  omega

theorem tall_witness (oldWidth width depth consumerFar : Int)
    (hwidth : 12 ≤ width) (hconsumer : 4 ≤ consumerFar ∧ consumerFar ≤ depth-10) :
    oldWidth+(width+8)+14 ≤ oldWidth+width+22 ∧ consumerFar+4 ≤ depth-6 ∧
    4 ≤ (oldWidth+width+22)-oldWidth-18 ∧ 4 ≤ (oldWidth+width+22)-oldWidth-12 := by
  omega

theorem original_charge (height legHalf : Int) (hheight : height % 2 = 0) :
    (height+legHalf-1)+legHalf-2*(height/2+legHalf) = -1 := by
  omega

theorem marginal (count : Int) (heven : count % 2 = 0) :
    1+2*(count/2)-3*count/2 = 1-count/2 := by
  omega

theorem joint_ledger (oldWidth width breadth : Int)
    (hold : oldWidth % 2 = 0) (hbreadth : breadth % 2 = 0) :
    (oldWidth+width+breadth+25)+1+2*(8+(oldWidth+breadth+12)/2)-
      (17+3*(oldWidth+breadth+12)/2) = oldWidth/2+width+breadth/2+19 := by
  omega

theorem joint_ge_forty (oldWidth width breadth : Int)
    (hold : 12 ≤ oldWidth) (hwidth : 12 ≤ width) (hbreadth : 6 ≤ breadth) :
    40 ≤ oldWidth/2+width+breadth/2+19 := by
  omega

theorem explicit_loss : 1-(12+6+12)/2 = (-14 : Int) ∧
    12/2+12+6/2+19 = (40 : Int) := by
  omega

end SubQuorum.SecondaryTenRootFourthConsumer
