"""
Common Helper utilities for transformers
"""
from sys import maxsize as BIG_NUMBER


def get_field_on_block(block, field_name, default_value=None):
    """
    Get the field value that is directly set on the xblock.
    Do not get the inherited value since field inheritance
    returns value from only a single parent chain
    (e.g., doesn't take a union in DAGs).
    """
    try:
        if block.fields[field_name].is_set_on(block):
            return getattr(block, field_name)
    except KeyError:
        pass
    return default_value


def collect_nearest_subsection(
        block_structure,
        transformer,
):
    """
    TODO: take another editing pass at this docstring before merge
    A very specialized (as in, I ought to see if we can generalize this or move it to the grading transformer's file)
    collect method designed to calculate and store the nearest containing subsection for every block in the course
    tree. This is done in 2 passes - the first will calculate and store a tuple, 'nearest_sub_dict', for each block
    in a topological traversal of the tree. This tuple will store the closest containing subsection and its distance
    from the block. On the second pass, we remove 'nearest_sub_dict' and only store the actual containing subsection,
    where one exists.
    """
    for block_key in block_structure.topological_traversal():
        if block_key.block_type == 'sequential':
            block_structure.set_transformer_block_field(
                block_key,
                transformer,
                'nearest_sub_dict',
                (0, block_key)
            )
            continue
        parent_data = [
            block_structure.get_transformer_block_field(
                parent,
                transformer,
                'nearest_sub_dict',
                (BIG_NUMBER, None),
            ) for parent in block_structure.get_parents(block_key)
        ]
        nearest = (BIG_NUMBER, None)
        for result_pair in parent_data:
            if result_pair[1] and result_pair[0] < nearest[0]:
                nearest = result_pair
        if nearest[1]:
            nearest = (nearest[0] + 1, nearest[1])
        block_structure.set_transformer_block_field(
            block_key,
            transformer,
            'nearest_sub_dict',
            nearest,
        )

    for block_key in block_structure.topological_traversal():
        nearest = block_structure.get_transformer_block_field(
            block_key,
            transformer,
            'nearest_sub_dict',
            (BIG_NUMBER, None),
        )
        block_structure.remove_transformer_block_field(
            block_key,
            transformer,
            'nearest_sub_dict'
        )
        if nearest[1]:
            block_structure.set_transformer_block_field(
                block_key,
                transformer,
                'containing_subsection',
                nearest[1],
            )


def collect_merged_boolean_field(
        block_structure,
        transformer,
        xblock_field_name,
        merged_field_name,
):
    """
    Collects a boolean xBlock field of name xblock_field_name
    for the given block_structure and transformer.  The boolean
    value is percolated down the hierarchy of the block_structure
    and stored as a value of merged_field_name in the
    block_structure.

    Assumes that the boolean field is False, by default. So,
    the value is ANDed across all parents for blocks with
    multiple parents and ORed across all ancestors down a single
    hierarchy chain.
    """

    for block_key in block_structure.topological_traversal():
        # compute merged value of the boolean field from all parents
        parents = block_structure.get_parents(block_key)
        all_parents_merged_value = all(  # pylint: disable=invalid-name
            block_structure.get_transformer_block_field(
                parent_key, transformer, merged_field_name, False,
            )
            for parent_key in parents
        ) if parents else False

        # set the merged value for this block
        block_structure.set_transformer_block_field(
            block_key,
            transformer,
            merged_field_name,
            (
                all_parents_merged_value or
                get_field_on_block(
                    block_structure.get_xblock(block_key), xblock_field_name,
                    False,
                )
            )
        )


def collect_merged_date_field(
        block_structure,
        transformer,
        xblock_field_name,
        merged_field_name,
        default_date,
        func_merge_parents=min,
        func_merge_ancestors=max,
):
    """
    Collects a date xBlock field of name xblock_field_name
    for the given block_structure and transformer.  The date
    value is percolated down the hierarchy of the block_structure
    and stored as a value of merged_field_name in the
    block_structure.
    """

    for block_key in block_structure.topological_traversal():

        parents = block_structure.get_parents(block_key)
        block_date = get_field_on_block(block_structure.get_xblock(block_key), xblock_field_name)
        if not parents:
            # no parents so just use value on block or default
            merged_date_value = block_date or default_date

        else:
            # compute merged value of date from all parents
            merged_all_parents_date = func_merge_parents(
                block_structure.get_transformer_block_field(
                    parent_key, transformer, merged_field_name, default_date,
                )
                for parent_key in parents
            )

            if not block_date:
                # no value on this block so take value from parents
                merged_date_value = merged_all_parents_date

            else:
                # compute merged date of the block and the parent
                merged_date_value = func_merge_ancestors(merged_all_parents_date, block_date)

        block_structure.set_transformer_block_field(
            block_key,
            transformer,
            merged_field_name,
            merged_date_value
        )
