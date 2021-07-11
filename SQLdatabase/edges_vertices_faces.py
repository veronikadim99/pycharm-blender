def edges_vertices_faces(current_object: object, database: object, drop_table: bool):
    """
        The function iterates through the edges,vertices and faces of the desired object and creates a table, where
        they are being stored
        :parameter: current_object: object which edges,vertices and faces are being stored
                    database: object the database where the new table will be created
                    drop_table: bool if True the table will be dropped if it already exists

        :return: None
    """

    cursor = database.cursor()

    if drop_table:
        drop = "DROP TABLE IF EXISTS {}".format("vertices_" + current_object.name)
        cursor.execute(drop)
        drop = "DROP TABLE IF EXISTS {}".format("edges_" + current_object.name)
        cursor.execute(drop)
        drop = "DROP TABLE IF EXISTS {}".format("faces_" + current_object.name)
        cursor.execute(drop)
    # create table for vertices
    data = "CREATE TABLE IF NOT EXISTS {} (vertex VARCHAR(40), x VARCHAR(50),y VARCHAR(50),z VARCHAR(50) )".format \
        ("vertices_" + current_object.name)
    cursor.execute(data)

    # create table for edges
    cursor.execute(
        'create table if not exists %s (`edge` varchar(40), `first` varchar(50),`second` varchar(50))' % str
        ('edges_' + current_object.name))

    # create table for faces
    cursor.execute \
        ('create table if not exists %s (`face` varchar(40), `f` varchar(5000))' % str('faces_' + current_object.name))

    # add vertices to table
    for vertex in current_object.data.vertices:
        data2 = [
            (vertex.index, vertex.co[0], vertex.co[1], vertex.co[2]),
        ]
        stmt2 = "INSERT INTO {} (vertex, x, y, z) VALUES (%s, %s, %s, %s)".format('vertices_' + current_object.name)
        cursor.executemany(stmt2, data2)

    # add edges to table
    for edge in current_object.data.edges:
        data3 = [
            (edge.index, edge.vertices[0], edge.vertices[1]),
        ]
        stmt3 = "INSERT INTO {} (edge, first, second) VALUES (%s, %s, %s)".format('edges_' + current_object.name)
        cursor.executemany(stmt3, data3)

    # add faces to table
    for poly in current_object.data.polygons:
        face = []
        for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
            face.append(current_object.data.loops[loop_index].vertex_index)
        f = str(face)
        f = f.strip("[]")
        data4 = [
            (poly.index, f),
        ]
        stmt4 = "INSERT INTO {} (face, f) VALUES (%s, %s)".format('faces_' + current_object.name)
        cursor.executemany(stmt4, data4)

    database.commit()

    cursor.close()

