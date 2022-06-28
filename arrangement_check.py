"""Astrovalidate check"""

from maya import cmds


class MayaModelCheck():
    """Class including all the necessary checks required for the task."""

    @staticmethod
    def distance_bw_points(p_1, p_2):
        """
        Return magnitude of distance between 2 positions.

        Args:
            p_1,p_2 (list): List of position vector coordinates.

        Returns:
            int: Magnitude of distance.
        """
        mag = (
            ((p_1[0] - p_2[0]) ** 2)
            + ((p_1[1] - p_2[1]) ** 2)
            + ((p_1[2] - p_2[2]) ** 2)
        )
        mag = mag ** 0.5
        return mag

    @staticmethod
    def magnitude(vec):
        """
        Return magnitude of vector.

        Args:
            vec (list): List of vector coordinates.

        Returns:
            int: Magnitude of distance.
        """
        mag = (vec[0] ** 2) + (vec[1] ** 2) + (vec[2] ** 2)
        mag = mag ** 0.5
        return mag

    @staticmethod
    def get_position(obj):
        """
        Return position vector of an object.

        Args:
            obj (str): Name/DAG path of the object.

        Returns:
            list: List of vector coordinates.
        """
        t_x = cmds.getAttr("{0}.tx".format(obj))
        t_y = cmds.getAttr("{0}.ty".format(obj))
        t_z = cmds.getAttr("{0}.tz".format(obj))
        return [t_x, t_y, t_z]

    @staticmethod
    def vector_bw_obj(v_1, v_2):
        """
        Return magnitude of distance between 2 positions.

        Args:
            v_1,v_2 (list): List of position vector coordinates.

        Returns:
            list: List of vector coordinates.
        """
        i = v_2[0] - v_1[0]
        j = v_2[1] - v_1[1]
        k = v_2[2] - v_1[2]
        vector = [i, j, k]
        return vector

    def distance_from_center(self, obj):
        """
        Return magnitude of distance from origin.

        Args:
            obj (str): Name/DAG path of the object.

        Returns:
            int: Magnitude of distance.
        """
        position = self.get_position(obj)
        distance = self.distance_bw_points([0, 0, 0], position)
        return distance

    @staticmethod
    def cross_product(v_1, v_2):
        """
        Return cross product of two vectors.

        Args:
            v_1,v_2 (list): List of position vector coordinates.

        Returns:
            list: List of vector coordinates.
        """
        i = ((v_1[1] * v_2[2]) - (v_1[2] * v_2[1]))
        j = ((v_1[2] * v_2[0]) - (v_1[0] * v_2[2]))
        k = ((v_1[0] * v_2[1]) - (v_1[1] * v_2[0]))
        product = [i, j, k]
        return product

    @staticmethod
    def get_faces(obj):
        """
        Return number of faces for an object.

        Args:
            obj (str): Name/DAG path of the object.

        Returns:
            int: Count for faces.
        """
        faces = cmds.polyEvaluate("{0}".format(obj), face=True)
        return faces

    def check_if_in_line(self, obj_list):
        """
        Check if the objects are in a single line.

        Args:
            obj_list (list): List of objects to perform the check.

        Returns:
            boolean: True or False as check result.
        """
        objs_position = []
        cross_product_result = []
        vector_bw_obj = []
        cross_products = []
        for obj in obj_list:
            position = self.get_position(obj)
            objs_position.append(position)

        for i in range(len(objs_position) - 1):
            new_vector = self.vector_bw_obj(
                objs_position[i],
                objs_position[i + 1]
            )
            vector_bw_obj.append(new_vector)

        for i in range(len(vector_bw_obj) - 1):
            product = self.cross_product(
                vector_bw_obj[i],
                vector_bw_obj[i + 1]
            )
            cross_products.append(product)
            magnitude = self.magnitude(product)
            if magnitude == 0:
                cross_product_result.append(True)
            else:
                cross_product_result.append(False)
        if False in cross_product_result:
            return False
        return True

    def if_equally_spaced(self, obj_list):
        """
        Check if the objects are equidistant from each other.

        Args:
            obj_list (list): List of objects to perform the check.

        Returns:
            boolean: True or False as check result.
        """
        distance_from_origin = []
        for obj in obj_list:
            position = self.get_position(obj)
            magnitude = self.magnitude(position)
            distance_from_origin.append(magnitude)
        distance_from_origin.sort()
        difference = distance_from_origin[1] - distance_from_origin[0]
        check = []
        for i in range(len(distance_from_origin) - 1):
            value = distance_from_origin[i + 1] - distance_from_origin[i]
            if value == difference:
                check.append(True)
            else:
                check.append(False)

        if False in check:
            return False
        return True

    def if_right_order(self, obj_list):
        """
        Check if sphere and poly with same index are well arranged.

        Args:
            obj_list (list): List of objects to perform the check.

        Returns:
            boolean: True or False as check result.
        """
        for obj in obj_list:
            if "pSphere" in obj:
                index = obj[-1]
                solid_name = "pSolid" + str(index)
                for obj2 in obj_list:
                    if solid_name in obj2:
                        if (self.distance_from_center(obj2)
                                < self.distance_from_center(obj)):
                            return False
        return True

    def if_right_order_poly(self, obj_list):
        """
        Check if polysolids with more faces are further from origin.

        Args:
            obj_list (list): List of objects to perform the check.

        Returns:
            boolean: True or False as check result.
        """
        polysolids = []
        for obj in obj_list:
            if "pSolid" in obj:
                polysolids.append(obj)
        for i in range(len(polysolids) - 1):
            if (self.get_faces(polysolids[i])
                    > self.get_faces(polysolids[i + 1])):
                return False

        return True

    def distance_for_furthestsphere(self, obj_list):
        """
        Return distance from center for furthest sphere.

        Args:
            obj_list (list): List of objects to inspect.

        Returns:
            int: Magnitude of distance.
        """
        sphere = []
        for obj in obj_list:
            if "pSphere" in obj:
                sphere.append(obj)

        sphere.sort(key=self.distance_from_center)
        fixed_distance = self.distance_from_center(sphere[-1])
        return fixed_distance

    @staticmethod
    def no_of_spheres(obj_list):
        """
        Return number of spheres in the object list.

        Args:
            obj_list (list): List of objects to inspect.

        Returns:
            int: Number of spheres.
        """
        sphere = []
        for obj in obj_list:
            if "pSphere" in obj:
                sphere.append(obj)
        no_of_spheres = int(len(sphere))
        return no_of_spheres

    def new_order_for_fixed_arrangement(self, obj_list):
        """
        Return number of spheres in the object list.

        Args:
            obj_list (list): List of objects to order.

        Returns:
            list: List of order for object arrangement.
        """
        spheres = []
        solids = []
        for obj in obj_list:
            if "Sphere" in obj:
                spheres.append(obj)
            else:
                solids.append(obj)
        spheres.sort(key=self.distance_from_center)
        solids.sort(key=self.get_faces)
        new_order = spheres + solids
        return new_order

    def fix_arrangement(self, obj_list):
        """
        Fix and arrange correctly.

        Args:
            obj_list (list): List of objects to fix.
        """
        distance = self.distance_for_furthestsphere(obj_list)
        no_of_spheres = self.no_of_spheres(obj_list)
        new_spacing_bw_objs = distance / no_of_spheres
        order = self.new_order_for_fixed_arrangement(obj_list)

        for i, i_1 in enumerate(order):
            cmds.setAttr(
                i_1 + ".translateX",
                new_spacing_bw_objs * (i + 1)
            )
            cmds.setAttr(order[i] + ".translateY", 0)
            cmds.setAttr(order[i] + ".translateZ", 0)


astro_check = MayaModelCheck()


def arrangement_check_and_fix():
    """
    Perform a check for fixed conditions.

    The correct arrangement satisfies:
        * the objects are evenly spaced
        * spheres are always closer to the origin
        than the polyhedron with the same index.
        * a polyhedron with more faces is always further from the origin.
        * the sphere"s distance from the origin stays the same.
        * warn if the objects are not in a straight line
    """
    obj_list = cmds.listRelatives(fullPath= True, allDescendents = False)
    for descendents in obj_list:
        if "Shape" in descendents:
            obj_list.remove(descendents)
    obj_list.sort(key=astro_check.distance_from_center)

    are_object_equally_spaced = astro_check.if_equally_spaced(obj_list)
    are_object_in_line = astro_check.check_if_in_line(obj_list)
    are_in_right_order2 = astro_check.if_right_order_poly(obj_list)
    are_in_right_order = astro_check.if_right_order(obj_list)

    if not are_object_equally_spaced:
        astro_check.fix_arrangement(obj_list)
        print("Objects were not equally spaced and are fixed",)

    if not are_object_in_line:
        astro_check.fix_arrangement(obj_list)
        print("Objects were not in one line and are fixed",)

    if not (are_in_right_order or are_in_right_order2):
        astro_check.fix_arrangement(obj_list)
        print("Objects were not in right order and are fixed",)

if __name__ == "__main__":
    arrangement_check_and_fix()
    
