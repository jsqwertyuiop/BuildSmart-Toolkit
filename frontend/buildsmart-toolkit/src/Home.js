import { HeaderSection } from "./components/Header.js";
import { Query } from "./components/Query.js";

export function Home(props) {
  return (
    <div>
      <HeaderSection />
      <Query />
    </div>
  );
}