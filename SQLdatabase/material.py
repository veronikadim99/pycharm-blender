def material(current_object: object, database: object, drop_table: bool):
    """
        The function iterates through the materials of the desired object and creates a table, where their name and
        texture are being stored
        :parameter: current_object: object which materials are being stored
                    database: object the database where the new table will be created
                    drop_table: bool if True the table will be dropped if it already exists

        :return: None
        """
    cursor = database.cursor()
    if drop_table:
        drop = "DROP TABLE IF EXISTS material_{}".format(current_object.name)
        cursor.execute(drop)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS material_{} (material_name VARCHAR(1600),texture_name VARCHAR(50)) ".format(
            current_object.name))
    for mat_slot in current_object.material_slots:
        # insert the name of the material in the table
        if mat_slot.material:
            if mat_slot.material.node_tree:
                stmt2 = "INSERT INTO {} (material_name) VALUES ('%s')".format(
                    'material_' + current_object.name) % mat_slot.name
                cursor.execute(stmt2)

                for x in mat_slot.material.node_tree.nodes:
                    # check if the material has an image texture and store it in the
                    # texture_name column for the current material
                    if x.type == 'TEX_IMAGE':
                        stmt2 = "UPDATE material_{0} SET texture_name = '%s' WHERE material_name = '%s'".format(
                            current_object.name)

                        cursor.execute(stmt2 % (x.image.name, mat_slot.name))

    database.commit()

    print(cursor.rowcount, "record inserted.")
    cursor.close()
