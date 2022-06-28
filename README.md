# Maya-astro-check
Astro checks are scripts that artists run on their scenes before dispatching them. The purpose of these checks is to validate what the artists are submitting to the publishing process and fix and/or flag any issue that we know can produce bad data down the pipeline. It varies pipeline to pipeline, this check validate if meshes and shapes are arranged correctly in a Maya scene.

The check perform these fixed conditions:

The correct arrangement satisfies:
    * the objects are evenly spaced
    * spheres are always closer to the origin than the polyhedron with the same index.
    * a polyhedron with more faces is always further from the origin.
    * the sphere"s distance from the origin stays the same.
    * warn if the objects are not in a straight line.
