import pywavefront

wavefront = pywavefront.Wavefront('sphere/uv_sphere.obj')
parsedObject = pywavefront.ObjParser(wavefront, wavefront.file_name)

print 'MESH>>>>'
print parsedObject.mesh

print 'MATERIAL>>>>'
print parsedObject.material

print 'VERTEX>>>>'
print parsedObject.vertices

print 'NORMIES>>>>'
print parsedObject.normals

print 'TEXTURES>>>>'
print parsedObject.tex_coords

