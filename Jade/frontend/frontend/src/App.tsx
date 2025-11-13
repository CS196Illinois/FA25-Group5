import ListGroup from "./components/ListGroup";
import Alert from "./components/Alert";
import Button from "./components/Button";

function App() {

  let items = ["NY", "SF", "Tokyo", "London", "Paris"];
  const handleSelectItem = (item: string) => {
    console.log(item);
  }

  return (
    <div>
      <Alert children="helo world" />
      <ListGroup items={items} heading="Preferences" onSelectItem={handleSelectItem}/>
      <Button></Button>
    </div>
  );
}

export default App;
