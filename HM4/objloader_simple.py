class OBJ:
    def __init__(self, filename, swapyz=False):
        self.vertices = []
        self.normals = []
        self.textures = []
        self.faces = []
        
        self.material = None
        self.materials = {}
        
        material = None
        
        for line in open(filename, "r"):
            if line.startswith('#'):
                continue
            
            if line.startswith('mtllib'):
                mtllib = line.replace('mtllib', '').strip()
                self.load_mtl(mtllib)
                continue
            
            if line.startswith('usemtl'):
                material = line.replace('usemtl', '').strip()
                continue
            
            if line.startswith('v '):
                x, y, z = map(float, line.split()[1:4])
                if swapyz:
                    self.vertices.append((x, z, -y))
                else:
                    self.vertices.append((x, y, z))
            
            elif line.startswith('vn '):
                nx, ny, nz = map(float, line.split()[1:4])
                if swapyz:
                    self.normals.append((nx, nz, -ny))
                else:
                    self.normals.append((nx, ny, nz))
            
            elif line.startswith('vt '):
                u, v = map(float, line.split()[1:3])
                self.textures.append((u, v))
            
            elif line.startswith('f '):
                # Face
                face = []
                textures = []
                norms = []
                
                for c_indices in line.split()[1:]:
                    c_split = c_indices.split('/')
                    c_index = int(c_split[0])
                    
                    face.append(c_index)
                    
                    if len(c_split) > 1 and c_split[1]:
                        textures.append(int(c_split[1]))
                    if len(c_split) > 2:
                        norms.append(int(c_split[2]))
                
                self.faces.append(face)
        
        self.gl_list = None
        self.material = material
    
    def load_mtl(self, filename):
        try:
            for line in open(filename, "r"):
                if line.startswith('newmtl'):
                    material_name = line.replace('newmtl', '').strip()
                    self.materials[material_name] = {}
        except:
            pass
