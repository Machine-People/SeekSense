import "../styles/app.css";


function SearchBar({ search, setSearch, onSearch }) {
  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Search by title, department, etc."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        onKeyDown={(e => {
            if (e.key === "Enter") {
                onSearch();
            }
        })
        }
      />
      <button onClick={onSearch}>Search</button>
    </div>
  );
}

export default SearchBar;
