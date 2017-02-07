import pywavefront

wavefront = pywavefront.Wavefront('uv_sphere.obj')
parsedObject = pywavefront.ObjParser(wavefront, wavefront.file_name)

#print parsedObject.mesh
#print parsedObject.material
print parsedObject.vertices
#print parsedObject.normals
print parsedObject.tex_coords

