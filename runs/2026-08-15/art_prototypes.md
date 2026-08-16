# ART PROTOTYPES — 2026-08-15 — before any dossier was written

Instinct 0.90 says prototype the hero through the REAL gates before the
storyboard exists, because run No.33's gate failed four of its six scratch
compositions and the dossiers were written against the two that passed. Four
prototypes were rendered and gate-tested here. The findings below are binding
on every dossier in this run's storyboard.

Files: `out/2026-08-15/proto/slides/` and `out/2026-08-15/proto/render/`.

## P0. The GPU is available and it is worth using

`examples/proof-3d` rendered clean in 6.1 s per slide. akthree PBR, IBL,
PCFSoft shadows and ACES all work in this container. Rung 1 of the rendered
ladder is open, and the last four decks all sat on rungs 2 and 3.

## P1. Transparent GL over a graded 2D atmosphere WORKS, and the grade order matters

`AKT.setup` does not expose `alpha`, and `getContext` fixes a canvas's
attributes forever, so the offscreen canvas gets its context created FIRST:

    off.getContext('webgl2',{alpha:true,premultipliedAlpha:true,
                             antialias:true,preserveDrawingBuffer:true});
    const R=AKT.setup(off,{w:1080,h:1350,exposure:1.02});
    R.renderer.setClearColor(0x000000,0);

With that, the rendered object composites onto the 2D atmosphere with no black
box behind it. `AKPOST.grade` runs on the 2D layer BEFORE the composite and
costs about a second; run after the GL pixels land it costs about 34.

The hand-drawn LIT APRON, a warm radial pool under the object with the contact
shadow multiplied into it, measured **dL 17.2 at feed scale** against a 4.0
floor and an 8.0 warn. It works. It is also unnecessary once the floor is
rendered, see P2.

The defect P1 shipped: the object FLOATS. The 2D pool and the hand-drawn
ellipse are at fixed y while the object's base is wherever the camera put it,
and a horizontal band edge at y=1075 reads as a strip rather than a ground.

## P2. A rendered floor fixes the float and FAILS the composition gate

Putting `AKT.ground` in the scene and dropping the camera to y=1.55 gives a
real horizon, real perspective falloff and a real PCFSoft contact shadow. The
object sits. The picture is much better.

    FAIL top-loaded composition: bottom third 15% of frame average
    FAIL contact shadow does not read: dL -0.9

Both failures are instructive.

The contact failure was MY RECTS, not the art. I declared the ground sample
300 px to the left of the shadow, on floor with different lighting. Instinct
0.95 exactly, a probe authored from predicted coordinates is not evidence.
Read the rects off the rendered PNG.

The composition failure is the real finding, below.

## P3. Answering the gate with scattered marks passes the gate and ruins the picture

Coarse mottle, 420 aggregate chips and perspective drafting furniture took the
bottom third from 15% to passing. The render then read as debris scattered on
a floor, with a hard seam where the 2D horizon disagreed with the GL one and a
wireframe rail floating over everything. **The gate was satisfied and the eye
was not.** This is the "flat furniture wearing a costume" defect in a new
costume, and it is worth recording that it is available and that it is wrong.

## P4. THE RECIPE. The floor is a MATERIAL, and the mass is composed low

    top 60% / mid 67% / bottom 41%   ratio 0.75, FAIL line 0.60

Two changes did it, both of them craft rather than gate-gaming.

**(a) The ground gets a procedural texture.** A smooth PBR plane has almost no
luminance spread inside a 27 design px cell, which is `frame_balance`'s cell
size, so the whole lower band reads as dead however well it is lit. A
canvas-generated fbm texture, stretched on one axis so it has a grain
direction, wrapped at `repeat(9,9)` and hung on the ground material, gives the
floor a real material. The gate and the picture improve together:

    const tc=document.createElement('canvas'); tc.width=tc.height=1024;
    // fbm2(x*0.010, y*0.055) stretched + fbm2(x*0.045, y*0.045) broken up
    const tex=new THREE.CanvasTexture(tc);
    tex.wrapS=tex.wrapT=THREE.RepeatWrapping; tex.repeat.set(9,9);
    tex.colorSpace=THREE.SRGBColorSpace;
    const gnd=AKT.ground(R,{color:0xffffff,y:0,size:70,roughness:0.86});
    gnd.material.map=tex; gnd.material.needsUpdate=true;

**(b) The mass is composed into the lower two thirds.** Hero at the middle and
lower thirds, a smaller companion further back for occlusion and scale, camera
low at y=1.35 looking at y=0.85. Type lives in the top third and nothing else
does.

## Binding rules for every dossier in this run

1. Every GL slide creates its offscreen context with `alpha:true` before
   `AKT.setup`, and calls `setClearColor(0x000000,0)`.
2. `AKPOST.grade` runs on the 2D layer BEFORE `drawImage` of the GL frame.
   Never after.
3. Any slide with a ground plane gives that ground a procedural canvas
   texture. A bare `AKT.ground` is a composition failure waiting to be
   reported.
4. Mass goes low. If the bottom third is holding only floor, the slide is
   already wrong and the gate will say so.
5. `data-contacts` rects are measured off the RENDERED PNG, never off the
   camera arithmetic, and the ground sample sits immediately beside the shadow
   on the same lighting.
6. The counter and any bottom-left tag must clear whatever furniture runs
   through the lower band. P3 failed on `03 / 03` being crossed by a rail and
   P4 failed on the counter colliding with the kicker at the top right. Park
   the counter where nothing else goes.
7. Two materials minimum on any hero object. The steel body against the gold
   collar reads instantly at thumb size; a single-material object does not.

## P5. THE HERO OBJECT, built and rendered before the dossier

A seated soft toy on a bench, built from akthree primitives, with exactly two
materials on the object and nothing else.

    FELT     AKT.mat.clay(0xC98468, {roughness:0.99})   body, head, ears
    FELT_D   AKT.mat.clay(0xA05F45, {roughness:0.99})   limbs, muzzle
    METAL    AKT.mat.steel({color:0x8A9AA8, roughness:0.30, metalness:0.95})
    DARK     MeshStandardMaterial 0x0B0E12, roughness 0.35, metalness 0.2

Geometry, all committed primitives, no external assets. Body a sphere at
r 0.92 scaled (1.0, 1.12, 0.94). Head a sphere at r 0.66. Ears spheres at
r 0.25 flattened to z 0.42. Arms and legs capsules. Eyes spheres at r 0.075 in
DARK. THE MACHINE IN THE CHEST is a metal torus bezel at r 0.30, a dark circle
face, and three concentric metal rings at r 0.072, 0.144 and 0.216, which is
the only cold material on the object and the whole thesis in one component.

Camera `from [2.05, 2.05, 5.35]`, `look [0, 1.35, 0]`, fov 50, rig
`arcticNight`, `objectHero` with `toward [6, 3.4, 5]`, keyColor 0xFFB070,
intensity 2.1, height 3.0.

**IT READS AT THUMB SIZE.** The silhouette is unmistakably a soft toy and the
dark disc on its chest is unmistakably not part of it. That is the deck's
argument delivered with no words, which is exactly what field 11a asks for.

### THE SEATING BUG, and it is a general one

`AKT.objectHero({height})` calls `fitHeight`, which rescales the group about
its ORIGIN. Whatever the group's own bounding box was, after that rescale its
minimum y is no longer 0, so the object hovers above the ground plane and every
critic reports the float. The fix is three lines and it belongs in every
dossier that scales a hero:

    AKT.objectHero(R, toy, {..., height: 3.0});
    toy.updateMatrixWorld(true);
    const bb = new THREE.Box3().setFromObject(toy);
    toy.position.y -= bb.min.y;

With that, the PCFSoft shadow map produces the contact for free and there is no
hand-drawn ellipse anywhere.

### Two tuning notes for the real slides

The bench texture at `repeat(10,10)` read as water. At `repeat(22,22)` it reads
as a brushed bench top. The felt at 0xD98F6B read too sweet for the subject and
was cooled to 0xC98468, so the warmth comes from the key rather than from the
pigment.

The headline overprinted the toy's head in both passes. On the real cover the
type block and the object get separate zones, and the counter goes where no
furniture runs.
