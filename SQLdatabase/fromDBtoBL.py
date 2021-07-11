import bpy


def create_object_from_db(object_name: str, database: object, collection: str):
    """
        The function iterates through all the tables in the database that exist for the desired object and reconstructs
        the object from the database information.
        :parameter: current_object: object we want to reconstruct
                    database: object the database where all of the object information is being stored
                    collection: str the name of the collection. Can be "Furniture 17" of "Furniture 13"

        :return: None
        """
    cursor = database.cursor()

    cursor.execute("USE blender;")
    # reconstruct the vertices from the database
    cursor.execute('SELECT * FROM {}'.format("vertices_" + object_name))
    verts = []
    for row in cursor:
        verts.append((float(row[1]), float(row[2]), float(row[3])))
    # reconstruct the edges from the database
    cursor.execute('SELECT * FROM {}'.format("edges_" + object_name))
    edges = []
    for row in cursor:
        edges.append([int(row[1]), int(row[2])])
    # reconstruct the faces from the database
    cursor.execute('SELECT * FROM {}'.format("faces_" + object_name))
    faces = []
    for row in cursor:
        vertices_in_face = row[1].split(",")
        face = []
        for v in vertices_in_face:
            face.append(int(v))
        faces.append(face)

    # add the new mesh to the right century
    mesh = bpy.data.meshes.new(object_name)
    obj = bpy.data.objects.new(mesh.name, mesh)
    col = bpy.data.collections.get(collection)
    col.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    mesh.from_pydata(verts, edges, faces)
    # reconstruct the coordinates from the database
    cursor.execute('SELECT location_x,location_y,location_z FROM {}'.format("coordinates_" + object_name))

    for row in cursor:
        obj.location[0] = row[0]
        obj.location[1] = row[1]
        obj.location[2] = row[2]

    cursor.execute('SELECT rotation_x,rotation_y,rotation_z FROM {}'.format("coordinates_" + object_name))

    for row in cursor:
        obj.rotation_euler[0] = row[0]
        obj.rotation_euler[1] = row[1]
        obj.rotation_euler[2] = row[2]
    cursor.execute('SELECT scale_x,scale_y,scale_z FROM {}'.format("coordinates_" + object_name))
    for row in cursor:
        obj.scale[0] = row[0]
        obj.scale[1] = row[1]
        obj.scale[2] = row[2]

    # assign the right material to the object
    cursor.execute('SELECT material_name,texture_name FROM {}'.format("material_" + object_name))

    for row in cursor:

        if row[0] is not None:
            mat = bpy.data.materials[row[0]]
            obj.data.materials.append(mat)

    mesh.uv_layers.new(name='NewUVMap_{}'.format(object_name))

    database.commit()

    cursor.close()
