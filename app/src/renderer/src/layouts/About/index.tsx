import { useEffect, useState } from "react";

function About() {
    const [version, setVersion] = useState('');
    useEffect(() => {
    async function fetchVersion() {
        const version = await window.api.getVersion();
        setVersion(version);
    }
    fetchVersion();
    }, []);
  return (
    <h5>
      autoMate v{version}
    </h5>
  );
}

export default About;