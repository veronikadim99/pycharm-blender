import bpy
import edges_vertices_faces, fromDBtoBL, coordinates, material
import mysql.connector
from bpy.props import EnumProperty
from bpy.types import Operator
from bpy.utils import register_class, unregister_class


def get_database():
    """
    The function connects with already existing database and returns it
    :parameter: None
    :return: the database in which the tables will be created
    """
    # replace the lines example_user and example_password with your username and password for mysql
    database = mysql.connector.connect(
        user="example_user",
        password="example_password",
        host="localhost",
        auth_plugin="mysql_native_password",
        database="blender"

    )
    return database


class CenturyPanel(bpy.types.Panel):
    """
        This class creates new panel with two buttons (one for each century) in blender

    """
    bl_label = "Century changer"
    bl_idname = "CC_TestPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Century'

    def draw(self, context):
        layout = self.layout
        layout.label(text="Change the century", icon='OBJECT_ORIGIN')

        layout.operator("button.button_op", text="17th century", icon='EVENT_S').action = 'seventeenth'

        layout.operator("button.button_op", text="13th century", icon='EVENT_T').action = 'thirteenth'


class Button_button_op(Operator):
    """
        This class reconstructs the objects for the century when a specific button is being pressed
    """
    bl_idname = 'button.button_op'
    bl_label = 'Century'
    bl_description = 'Change century'
    bl_options = {'REGISTER', 'UNDO'}
    database = mysql.connector.connect(
        user="example_username",
        password="example_password",
        host="localhost",
        auth_plugin="mysql_native_password",
        database="blender"

    )
    action: EnumProperty(
        items=[
            ('seventeenth', '17th century', '17th century'),
            ('thirteenth', '13th century', '13th century'),

        ]
    )

    def execute(self, context):
        """
            The function executes if one of the buttons is being pressed.
            ":return sequence that execution is finished
        """
        if self.action == 'seventeenth':
            self.seventeenth()
        else:
            self.thirteenth()

        return {'FINISHED'}

    @staticmethod
    def seventeenth():
        """
            The function reconstructs the objects for the 17th century where the fromDBtoBL script is being called
            :parameter: None

            :return: None
        """
        collection = bpy.data.collections['Furniture13']
        if len(bpy.data.collections['Furniture17'].objects) == 0 or bpy.context.view_layer.layer_collection.children[
            "Furniture17"].hide_viewport:
            for obj in collection.objects:
                bpy.data.objects.remove(obj)
            furniture17 = ["carpet17", "dinner_table17", "first_chair17", "second_chair17",
                           "third_chair17", "fourth_chair17", "gimble17", "painting1_17", "painting2_17", "frame1_17",
                           "frame2_17", "painting3_17", "frame3_17", "book1_17", "cover1_17", "candle1_17",
                           "candle2_17", "Walls17"]
            for obj_name in furniture17:
                fromDBtoBL.create_object_from_db(obj_name, get_database(), "Furniture17")
            if bpy.context.view_layer.layer_collection.children["Furniture17"].hide_viewport:
                bpy.context.view_layer.layer_collection.children["Furniture17"].hide_viewport = False

    @staticmethod
    def thirteenth():
        """
            The function reconstructs the objects for the 13th century where the fromDBtoBL script is being called
            :parameter: None

            :return: None
        """
        collection = bpy.data.collections['Furniture17']
        if len(bpy.data.collections['Furniture13'].objects) == 0 or bpy.context.view_layer.layer_collection.children[
            "Furniture13"].hide_viewport:
            for obj in collection.objects:
                bpy.data.objects.remove(obj)
            furniture13 = ["dinner_table13", "first_chair13", "second_chair13",
                           "third_chair13", "fourth_chair13", "gimble13", "carpet13", "painting1_13",
                           "painting2_13", "frame1_13", "frame2_13", "painting3_13", "frame3_13", "poster13",
                           "candle1_13", "candle2_13", "Walls13"]
            for obj_name in furniture13:
                fromDBtoBL.create_object_from_db(obj_name, get_database(), "Furniture13")

            if bpy.context.view_layer.layer_collection.children["Furniture13"].hide_viewport:
                bpy.context.view_layer.layer_collection.children["Furniture13"].hide_viewport = False


def register():
    """
        Register the buttons and their properties
        :parameter: None

        :return: None
    """
    register_class(Button_button_op)
    register_class(CenturyPanel)


def unregister():
    """
        Unregister the buttons and their properties
        :parameter: None

        :return: None
    """
    unregister_class(Button_button_op)
    unregister_class(CenturyPanel)


if __name__ == "__main__":
    database = get_database()
    # create two lists with the names of the objects
    furniture13 = ["dinner_table13", "first_chair13", "second_chair13",
                   "third_chair13", "fourth_chair13", "gimble13", "carpet13", "painting1_13",
                   "painting2_13", "frame1_13", "frame2_13", "painting3_13", "frame3_13", "poster13", "candle1_13",
                   "candle2_13", "Walls13"]
    furniture17 = ["carpet17", "dinner_table17", "first_chair17", "second_chair17",
                   "third_chair17", "fourth_chair17", "gimble17", "painting1_17", "painting2_17", "frame1_17",
                   "frame2_17", "painting3_17", "frame3_17", "book1_17", "cover1_17", "candle1_17", "candle2_17",
                   "Walls17"]
    cursor = database.cursor()

    # if the database is empty, create five tables for each object
    cursor.execute("SELECT COUNT(DISTINCT `table_name`) FROM `information_schema`.`columns` WHERE `table_schema` = "
                   "'blender'")
    data = cursor.fetchone()

    if data[0] == 0:
        for obj in bpy.data.collections['Furniture13'].objects:
            material.material(obj, database, True)
        for obj in bpy.data.collections['Furniture17'].objects:
            material.material(obj, database, True)
        for obj in bpy.data.collections['Furniture13'].objects:
            edges_vertices_faces.edges_vertices_faces(obj, database, True)
        for obj in bpy.data.collections['Furniture17'].objects:
            edges_vertices_faces.edges_vertices_faces(obj, database, True)
        for obj in bpy.data.collections['Furniture13'].objects:
            coordinates.coordinates(obj, database, True)
        for obj in bpy.data.collections['Furniture17'].objects:
            coordinates.coordinates(obj, database, True)
    print("All tables inserted")
    register()
    database.close()
