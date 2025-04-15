# System Patterns

## Architecture Overview
The Solax integration follows the standard Home Assistant integration architecture with a focus on the data update coordinator pattern. This ensures efficient data fetching and processing while providing a consistent update mechanism for all sensor entities.

## Key Components

### 1. Configuration Flow
- **Component**: `config_flow.py`
- **Pattern**: Home Assistant Config Flow
- **Purpose**: Handles the UI-based configuration of the integration
- **Key Features**:
  - Form-based configuration
  - Validation of connection parameters
  - Creation of config entries

### 2. Data Update Coordinator
- **Component**: `coordinator.py`
- **Pattern**: Home Assistant DataUpdateCoordinator
- **Purpose**: Central data fetching and processing hub
- **Key Features**:
  - Regular polling of the Solax API
  - Data parsing and processing
  - Error handling
  - Providing processed data to entities

### 3. Entity Framework
- **Component**: `entity.py`, `sensor.py`
- **Pattern**: Home Assistant Entity Model
- **Purpose**: Representation of data as Home Assistant entities
- **Key Features**:
  - Base entity implementation
  - Specialized sensor entities
  - Automatic updates from coordinator

### 4. Integration Setup
- **Component**: `__init__.py`
- **Pattern**: Home Assistant Integration Setup
- **Purpose**: Initialize and set up the integration
- **Key Features**:
  - Register the integration with Home Assistant
  - Set up the coordinator
  - Create platform entities

## Data Flow

```
[Solax Inverter API] <-- HTTP Requests --> [Data Update Coordinator]
                                                   |
                                                   v
                                           [Data Processing]
                                                   |
                                                   v
                                         [Entity Creation/Update]
                                                   |
                                                   v
                                    [Home Assistant State & Services]
```

1. The coordinator makes HTTP requests to the Solax inverter API
2. The API responds with data in text/HTML format containing JSON
3. The coordinator parses and processes the response
4. Sensor entities consume the processed data
5. Home Assistant displays the data and makes it available for automations, etc.

## Key Design Patterns

### 1. Dependency Injection
- The coordinator is instantiated in `__init__.py` and passed to entities
- This ensures a single source of truth for data

### 2. Observer Pattern
- Entities observe the coordinator for data updates
- When the coordinator updates, all entities are notified

### 3. Factory Pattern
- Sensor entities are created based on the available data
- Dynamic creation of sensors depending on inverter capabilities

### 4. Strategy Pattern
- Different processing strategies for different data types
- Allows for flexibility in handling various data formats

## Error Handling Strategy
1. Network errors are caught and logged
2. JSON parsing errors are handled with detailed logging
3. Missing or invalid data points are skipped
4. Configuration errors are presented clearly to the user

## Naming Conventions
- **Domain**: `custom-solax`
- **Entity IDs**: `sensor.solax_<sensor_name>`
- **Data Keys**: Match the Solax API with underscores for readability

## Extension Points
1. **Additional Sensor Types**: New sensor types can be added to `const.py`
2. **Enhanced Data Processing**: The `_process_data` method can be extended
3. **Alternative Connection Methods**: Could be implemented in the coordinator
4. **Additional Configuration Options**: Can be added to the config flow 