

def coordinates(current_object: object, database: object, drop_table: bool):
    """
            The function iterates through the coordinates of the desired object and creates a table, where
            the location, rotation and the scale of the object are being stored
            :parameter: current_object: object which coordinates are being stored
                        database: object the database where the new table will be created
                        drop_table: bool if True the table will be dropped if it already exists

            :return: None
            """
    cursor = database.cursor()
    if drop_table:
        drop = "DROP TABLE IF EXISTS {}".format("coordinates_" + current_object.name)
        cursor.execute(drop)
    # create the table
    cursor.execute("CREATE TABLE IF NOT EXISTS {} (name VARCHAR(50),location_x FLOAT,location_y "
                   "FLOAT, location_z FLOAT,rotation_x FLOAT,rotation_y FLOAT,"
                   "rotation_z FLOAT,scale_x FLOAT,scale_y FLOAT,scale_z FLOAT)"
                   "".format("coordinates_" + current_object.name))
    # get all of the coordinates the object has
    data = "INSERT INTO {} (name,location_x,location_y,location_z,rotation_x,rotation_y," \
           "rotation_z,scale_x,scale_y,scale_z) VALUES " \
           "(%s, %s, %s, %s,%s, %s, %s,%s, %s, %s)".format("coordinates_" + current_object.name)

    values = (current_object.name, current_object.location[0], current_object.location[1], current_object.location[2],
              current_object.rotation_euler[0], current_object.rotation_euler[1], current_object.rotation_euler[2],
              current_object.scale[0], current_object.scale[1], current_object.scale[2])

    cursor.execute(data, values)
    database.commit()
    print(cursor.rowcount, "record inserted.")
    cursor.close()




