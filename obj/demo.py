import pywavefront

wavefront = pywavefront.Wavefront('LibertyStatue/LibertStatue.obj')
parsedObject = pywavefront.ObjParser(wavefront, wavefront.file_name)

#print parsedObject.mesh
#print parsedObject.material
print parsedObject.vertices
#print parsedObject.normals
print parsedObject.tex_coords

