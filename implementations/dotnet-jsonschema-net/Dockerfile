FROM mcr.microsoft.com/dotnet/sdk:9.0.303 AS build
WORKDIR /source

COPY *.csproj .
RUN dotnet restore

COPY . .
RUN dotnet publish -c Release -o /app --no-restore

FROM mcr.microsoft.com/dotnet/runtime:9.0-alpine
WORKDIR /app
COPY --from=build /app .
ENTRYPOINT ["dotnet", "bowtie_json_everything.dll"]
