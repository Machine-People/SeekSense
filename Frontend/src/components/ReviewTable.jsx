import "../styles/app.css";



function ReviewTable({ reviews }) {
  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>ClothingID</th>
            <th>Title</th>
            <th>ReviewText</th>
            <th>Rating</th>
            <th>Division</th>
            <th>Department</th>
            <th>Class</th>
          </tr>
        </thead>
        <tbody>
          {reviews.length === 0 ? (
            <tr>
              <td colSpan="7" style={{ textAlign: "center", color: "gray" }}>
                No results found.
              </td>
            </tr>
          ) : (
            reviews.map((r, i) => (
              <tr key={i}>
                <td>{r.clothingid}</td>
                <td>{r.title}</td>
                <td>{r.reviewtext?.slice(0, 50)}...</td>
                <td>{r.rating}</td>
                <td>{r.divisionname}</td>
                <td>{r.departmentname}</td>
                <td>{r.classname}</td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}

export default ReviewTable;
