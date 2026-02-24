"use client";

import { CopilotChat } from "@copilotkit/react-ui";
import { useCopilotAction } from "@copilotkit/react-core";

function WeatherCard({
  location,
  temperature,
  feelsLike,
  humidity,
  windSpeed,
  windGust,
  conditions,
  isLoading,
}: {
  location?: string;
  temperature?: number;
  feelsLike?: number;
  humidity?: number;
  windSpeed?: number;
  windGust?: number;
  conditions?: string;
  isLoading: boolean;
}) {
  const tempF = temperature != null ? (temperature * 9 / 5 + 32).toFixed(1) : null;

  return (
    <div
      className={`rounded-lg border border-sky-300 bg-gradient-to-br from-sky-100 to-blue-100 p-4 max-w-xs shadow-md ${isLoading ? "animate-pulse" : ""}`}
    >
      <h3 className="text-lg font-semibold text-sky-700">
        {location || "Loading..."}
      </h3>
      <p className="text-xs text-sky-500 uppercase tracking-wide mb-3">
        {isLoading ? "Fetching weather..." : "Current Weather"}
      </p>

      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="text-4xl font-bold text-gray-800">
            {temperature != null ? temperature : "--"}
            <span className="text-lg text-sky-600">&deg;C</span>
          </div>
          {tempF && (
            <div className="text-sm text-gray-500">{tempF}&deg;F</div>
          )}
        </div>
        <div className="text-sm text-gray-500 text-right max-w-[120px]">
          {conditions || "--"}
        </div>
      </div>

      <div className="grid grid-cols-3 gap-2 pt-3 border-t border-sky-200">
        <div className="text-center">
          <div className="text-[10px] text-gray-500 uppercase">Humidity</div>
          <div className="text-sm font-mono text-gray-800">
            {humidity != null ? `${humidity}%` : "--%"}
          </div>
        </div>
        <div className="text-center">
          <div className="text-[10px] text-gray-500 uppercase">Wind</div>
          <div className="text-sm font-mono text-gray-800">
            {windSpeed != null ? `${windSpeed} km/h` : "-- km/h"}
          </div>
        </div>
        <div className="text-center">
          <div className="text-[10px] text-gray-500 uppercase">Feels Like</div>
          <div className="text-sm font-mono text-gray-800">
            {feelsLike != null ? `${feelsLike}\u00B0` : "--\u00B0"}
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  useCopilotAction({
    name: "get_weather",
    description: "Get the weather for a given location.",
    available: "disabled",
    parameters: [
      { name: "location", type: "string", required: true },
    ],
    render: ({ args, status, result }) => {
      if (status === "complete" && result) {
        let data = result;
        if (typeof result === "string") {
          try {
            data = JSON.parse(result.replace(/'/g, '"'));
          } catch {
            return <div>{result}</div>;
          }
        }
        return (
          <WeatherCard
            location={data.location}
            temperature={data.temperature}
            feelsLike={data.feelsLike}
            humidity={data.humidity}
            windSpeed={data.windSpeed}
            windGust={data.windGust}
            conditions={data.conditions}
            isLoading={false}
          />
        );
      }
      return <WeatherCard location={args.location} isLoading={true} />;
    },
  });

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-sky-100 to-blue-200">
      <div className="w-full max-w-2xl h-[80vh] rounded-xl overflow-hidden shadow-2xl border border-sky-300">
        <CopilotChat
          labels={{
            title: "AG2 Weather Agent",
            initial: "Hi! Ask me about the weather in any city.",
            placeholder: "Ask about the weather...",
          }}
          className="h-full"
        />
      </div>
    </div>
  );
}
