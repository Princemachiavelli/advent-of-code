<?php

// The grid of trees as a string
$grid_str = "30373\n25512\n65332\n33549\n35390";

// Parse the grid into a 2D array of integers
$grid = array_map(function($row) {
  return array_map('intval', str_split($row));
}, explode("\n", $grid_str));

// The number of visible trees
$num_visible = 0;

// Loop through each row and column of the grid
for ($row = 0; $row < count($grid); $row++) {
  for ($col = 0; $col < count($grid[$row]); $col++) {
    // Check if the tree at this position is visible
    if (isVisible($grid, $row, $col)) {
      // If it is visible, increment the count
      $num_visible++;
    }
  }
}

// Output the result
echo "There are $num_visible visible trees.\n";


/**
 * Determines whether a tree at a given position in the grid is visible
 *
 * @param array $grid The grid of trees as a 2D array of integers
 * @param int $row The row of the tree to check
 * @param int $col The column of the tree to check
 * @return bool True if the tree is visible, false otherwise
 */
function isVisible(array $grid, int $row, int $col): bool {
  // The height of the tree at this position
  $tree_height = $grid[$row][$col];

  // Check if there are any trees in the same row or column that are taller
  // than the tree at this position

  // Check the trees to the left of this tree
  for ($i = $col - 1; $i >= 0; $i--) {
    if ($grid[$row][$i] >= $tree_height) {
      return false;
    }
  }

  return true;

  // Check the trees to the right of this tree
  for ($i = $col + 1; $i < count($grid[$row]); $i++) {
    if ($grid[$row][$i] >= $tree_height) {
      return false;
    }
  }

  return true;
  // Check the trees above this tree
  for ($i = $row - 1; $i >= 0; $i--) {
    if ($grid[$i][$col] >= $tree_height) {
      return false;
    }
  }

  return true;
  // Check the trees below this tree
  for ($i = $row + 1; $i < count($grid); $i++) {
    if ($grid[$i][$col] >= $tree_height) {
      return false;
    }
  }

  // If no taller trees were found, this tree is visible
  return true;
}
