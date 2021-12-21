import React from 'react';

import Paginations from "components/Pagination/Pagination.jsx";

function Example({...props}){
  return (
    <Paginations
      pages={[
        { text: "PREV" },
        { text: 1 },
        { text: 2 },
        { active: true, text: 3 },
        { text: 4 },
        { text: 5 },
        { text: "NEXT" }
      ]}
      color="info"
    />
  );
}

export default Example;
Pagination.defaultProps = {
  color: "primary"
};

Pagination.propTypes = {
  pages: PropTypes.arrayOf(
    PropTypes.shape({
      active: PropTypes.bool,
      disabled: PropTypes.bool,
      text: PropTypes.oneOfType([
        PropTypes.number,
        PropTypes.oneOf(["PREV", "NEXT", "..."])
      ]).isRequired,
      onClick: PropTypes.func
    })
  ).isRequired,
  color: PropTypes.oneOf(["primary", "info", "success", "warning", "danger"])
};